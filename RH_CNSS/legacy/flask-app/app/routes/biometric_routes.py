"""
Rôle du fichier:
Expose les endpoints de gestion biométrique (empreintes digitales, RFID, pointage).
"""

from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Attendance, BiometricDevice, Employee
from app.utils.activity_logger import log_activity

biometric_bp = Blueprint("biometric", __name__)

BIOMETRIC_BRIDGE_URL = "http://localhost:5002"


def _read_bridge_api_key():
    """Lit la clé API du bridge depuis key.bin (chiffrée DPAPI)."""
    import ctypes, ctypes.wintypes, os
    key_path = os.path.join(os.environ.get("APPDATA", ""), "FingerprintBridge", "key.bin")
    if not os.path.exists(key_path):
        return None
    with open(key_path, "rb") as f:
        encrypted = f.read()
    # DPAPI CryptUnprotectData
    entropy_str = b"FingerprintBridgeEntropy_v1"

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    crypt = ctypes.windll.crypt32
    enc_blob = DATA_BLOB(len(encrypted), ctypes.cast(ctypes.c_char_p(encrypted), ctypes.POINTER(ctypes.c_char)))
    ent_blob = DATA_BLOB(len(entropy_str), ctypes.cast(ctypes.c_char_p(entropy_str), ctypes.POINTER(ctypes.c_char)))
    out_blob = DATA_BLOB()
    ok = crypt.CryptUnprotectData(
        ctypes.byref(enc_blob), None, ctypes.byref(ent_blob),
        None, None, 0, ctypes.byref(out_blob)
    )
    if not ok:
        return None
    result = ctypes.string_at(out_blob.pbData, out_blob.cbData).decode("utf-8")
    ctypes.windll.kernel32.LocalFree(out_blob.pbData)
    return result


@biometric_bp.post("/scan")
@jwt_required()
def proxy_scan():
    """Proxifie l'appel de scan d'empreinte vers le bridge local avec la vraie clé API."""
    import urllib.request, json as _json
    api_key = _read_bridge_api_key()
    if not api_key:
        return jsonify({"error": "Clé API bridge introuvable"}), 503
    try:
        # Désactiver le proxy système pour les appels localhost
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        req = urllib.request.Request(
            f"{BIOMETRIC_BRIDGE_URL}/scan",
            data=b"{}",
            headers={"Content-Type": "application/json", "X-API-KEY": api_key},
            method="POST",
        )
        with opener.open(req, timeout=30) as resp:
            data = _json.loads(resp.read())
        return jsonify(data), 200
    except urllib.error.HTTPError as e:
        try:
            body = _json.loads(e.read())
        except Exception:
            body = {"error": f"HTTP {e.code}"}
        return jsonify(body), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@biometric_bp.get("/status")
@jwt_required()
def bridge_status():
    """Vérifie la disponibilité du bridge biométrique local."""
    import urllib.request, json as _json
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(f"{BIOMETRIC_BRIDGE_URL}/status", timeout=2) as resp:
            return jsonify(_json.loads(resp.read())), 200
    except Exception:
        return jsonify({"connected": False, "message": "Bridge non disponible"}), 200


@biometric_bp.get("/enrolled")
@jwt_required()
def list_enrolled():
    """Retourne la liste des employés avec empreinte ou RFID enregistré."""
    employees = Employee.query.all()
    result = []
    for emp in employees:
        if emp.fingerprint_template or emp.rfid_card_id:
            result.append({
                "id": emp.id,
                "name": f"{emp.first_name} {emp.last_name}",
                "has_fingerprint": bool(emp.fingerprint_template),
                "rfid_card_id": emp.rfid_card_id,
                "rfid_card_active": emp.rfid_card_active,
            })
    return jsonify(result)


@biometric_bp.post("/enroll/<int:employee_id>")
@jwt_required()
def enroll_fingerprint(employee_id):
    """Enregistre le template d'empreinte digitale d'un employé."""
    emp = Employee.query.get_or_404(employee_id)
    data = request.get_json() or {}
    template = data.get("template")
    if not template:
        return jsonify({"error": "Template manquant"}), 400
    emp.fingerprint_template = template
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Empreinte enregistrée employé #{employee_id}")
    return jsonify({"message": "Empreinte enregistrée", "employee_id": employee_id})


@biometric_bp.post("/rfid/assign")
@jwt_required()
def assign_rfid():
    """Assigne une carte RFID à un employé."""
    data = request.get_json() or {}
    employee_id = data.get("employee_id")
    rfid_card_id = data.get("rfid_card_id")
    if not employee_id or not rfid_card_id:
        return jsonify({"error": "employee_id et rfid_card_id requis"}), 400
    emp = Employee.query.get_or_404(employee_id)
    emp.rfid_card_id = rfid_card_id
    emp.rfid_card_active = True
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"RFID assignée à employé #{employee_id}")
    return jsonify({"message": "RFID assignée", "employee_id": employee_id, "rfid_card_id": rfid_card_id})


@biometric_bp.post("/rfid/deactivate")
@jwt_required()
def deactivate_rfid():
    """Désactive la carte RFID d'un employé."""
    data = request.get_json() or {}
    employee_id = data.get("employee_id")
    emp = Employee.query.get_or_404(employee_id)
    emp.rfid_card_active = False
    db.session.commit()
    return jsonify({"message": "RFID désactivée"})


@biometric_bp.post("/checkin/rfid")
def checkin_rfid():
    """Enregistre un pointage via RFID (sans authentification — appelé par le périphérique)."""
    data = request.get_json() or {}
    rfid_card_id = data.get("rfid_card_id")
    emp = Employee.query.filter_by(rfid_card_id=rfid_card_id, rfid_card_active=True).first()
    if not emp:
        return jsonify({"error": "Carte non reconnue"}), 404
    att = Attendance(
        employee_id=emp.id,
        check_in=datetime.utcnow(),
        worked_hours=0,
        late_minutes=0,
        is_absent=False,
        source="rfid",
    )
    db.session.add(att)
    db.session.commit()
    return jsonify({"message": "Pointage enregistré", "employee": f"{emp.first_name} {emp.last_name}"})


@biometric_bp.post("/checkin/fingerprint")
def checkin_fingerprint():
    """Enregistre un pointage via empreinte digitale."""
    data = request.get_json() or {}
    employee_id = data.get("employee_id")
    emp = Employee.query.get_or_404(employee_id)
    att = Attendance(
        employee_id=emp.id,
        check_in=datetime.utcnow(),
        worked_hours=0,
        late_minutes=0,
        is_absent=False,
        source="fingerprint",
    )
    db.session.add(att)
    db.session.commit()
    return jsonify({"message": "Pointage empreinte enregistré"})


@biometric_bp.get("/devices")
@jwt_required()
def list_devices():
    """Liste les périphériques biométriques enregistrés."""
    devices = BiometricDevice.query.all()
    return jsonify([{
        "id": d.id,
        "name": d.name,
        "device_type": d.device_type,
        "location": d.location,
        "is_active": d.is_active,
        "last_seen": d.last_seen.isoformat() if d.last_seen else None,
    } for d in devices])
