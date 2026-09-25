"""
Routes biométriques — enrôlement empreintes digitales, attribution RFID,
pointage biométrique et gestion des dispositifs ZK-9500.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, date

import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import db
from app.models.db_models import Employee, Attendance, BiometricDevice
from app.exceptions import AppException

biometric_bp = Blueprint("biometric", __name__, url_prefix="/api/biometric")

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _get_device_or_404(device_id: int) -> BiometricDevice:
    device = db.session.get(BiometricDevice, device_id)
    if not device or not device.is_active:
        raise AppException("Dispositif biométrique introuvable ou inactif", 404)
    return device


def _call_bridge(device: BiometricDevice, endpoint: str, method: str = "POST", payload: dict | None = None):
    """Appelle le pont C# (fingerprint-service) tournant sur la machine locale."""
    if not device.bridge_url:
        raise AppException("URL du bridge non configurée pour ce dispositif", 400)
    url = device.bridge_url.rstrip("/") + endpoint
    headers = {}
    if device.api_key_hash:
        headers["X-API-KEY"] = device.api_key_hash
    try:
        if method == "POST":
            resp = requests.post(url, json=payload or {}, headers=headers, timeout=15)
        else:
            resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise AppException("Impossible de joindre le bridge biométrique. Vérifiez que fingerprint-service est lancé.", 503)
    except requests.exceptions.Timeout:
        raise AppException("Le bridge biométrique n'a pas répondu dans les délais.", 504)
    except requests.exceptions.HTTPError as exc:
        raise AppException(f"Erreur du bridge: {exc.response.status_code}", exc.response.status_code)


# -------------------------------------------------------------------
# Dispositifs biométriques
# -------------------------------------------------------------------

@biometric_bp.get("/devices")
@jwt_required()
def list_devices():
    devices = BiometricDevice.query.all()
    return jsonify([{
        "id": d.id,
        "name": d.name,
        "device_type": d.device_type,
        "location": d.location,
        "is_active": d.is_active,
        "bridge_url": d.bridge_url,
        "last_seen": d.last_seen.isoformat() if d.last_seen else None,
        "created_at": d.created_at.isoformat(),
    } for d in devices])


@biometric_bp.post("/devices")
@jwt_required()
def create_device():
    claims = get_jwt()
    perms = claims.get("permissions", [])
    if "manage_biometric_devices" not in perms and "admin_all" not in perms:
        raise AppException("Permission refusée", 403)

    data = request.get_json(force=True)
    name = data.get("name", "").strip()
    if not name:
        raise AppException("Le nom du dispositif est requis", 400)

    device = BiometricDevice(
        name=name,
        device_type=data.get("device_type", "fingerprint"),
        location=data.get("location"),
        bridge_url=data.get("bridge_url"),
        api_key_hash=data.get("api_key"),
    )
    db.session.add(device)
    db.session.commit()
    return jsonify({"id": device.id, "message": "Dispositif créé"}), 201


@biometric_bp.get("/devices/<int:device_id>/status")
@jwt_required()
def device_status(device_id: int):
    device = _get_device_or_404(device_id)
    try:
        result = _call_bridge(device, "/status", method="GET")
        device.last_seen = datetime.utcnow()
        db.session.commit()
        return jsonify({"online": True, "bridge_status": result})
    except AppException as exc:
        return jsonify({"online": False, "error": exc.message}), 200


# -------------------------------------------------------------------
# Enrôlement empreinte digitale
# -------------------------------------------------------------------

@biometric_bp.post("/enroll/<int:employee_id>")
@jwt_required()
def enroll_fingerprint(employee_id: int):
    """
    Déclenche une lecture d'empreinte sur le dispositif indiqué,
    puis stocke le template base64 dans le dossier de l'employé.
    Body JSON: { "device_id": 1 }
    """
    claims = get_jwt()
    perms = claims.get("permissions", [])
    if "manage_biometric_devices" not in perms and "admin_all" not in perms:
        raise AppException("Permission refusée", 403)

    employee = db.session.get(Employee, employee_id)
    if not employee:
        raise AppException("Employé introuvable", 404)

    data = request.get_json(force=True)
    device_id = data.get("device_id")
    if not device_id:
        raise AppException("device_id requis", 400)

    device = _get_device_or_404(device_id)
    result = _call_bridge(device, "/scan")

    template = result.get("template")
    if not template:
        raise AppException("Le bridge n'a pas retourné de template d'empreinte", 502)

    employee.fingerprint_template = template
    device.last_seen = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "message": f"Empreinte enrôlée pour {employee.first_name} {employee.last_name}",
        "employee_id": employee_id,
    })


# -------------------------------------------------------------------
# Vérification / pointage par empreinte
# -------------------------------------------------------------------

@biometric_bp.post("/verify")
@jwt_required()
def verify_fingerprint():
    """
    Scan une empreinte sur le dispositif, la compare à la galerie,
    et enregistre le pointage de l'employé identifié.
    Body JSON: { "device_id": 1, "event_type": "check_in" | "check_out" }
    """
    data = request.get_json(force=True)
    device_id = data.get("device_id")
    event_type = data.get("event_type", "check_in")

    if not device_id:
        raise AppException("device_id requis", 400)

    device = _get_device_or_404(device_id)

    # 1. Scan de l'empreinte live
    scan_result = _call_bridge(device, "/scan")
    probe_template = scan_result.get("template")
    if not probe_template:
        raise AppException("Echec de la capture d'empreinte", 502)

    # 2. Construire la galerie depuis la base de données
    employees_with_fp = Employee.query.filter(Employee.fingerprint_template.isnot(None)).all()
    gallery = [
        {"employee_id": e.id, "template": e.fingerprint_template}
        for e in employees_with_fp
    ]

    if not gallery:
        raise AppException("Aucune empreinte enrôlée dans le système", 404)

    # 3. Matching via le bridge
    match_result = _call_bridge(device, "/match", payload={
        "probe_template": probe_template,
        "gallery": gallery,
    })

    matched_employee_id = match_result.get("employee_id")
    if not matched_employee_id:
        return jsonify({"matched": False, "message": "Empreinte non reconnue"}), 200

    employee = db.session.get(Employee, matched_employee_id)
    device.last_seen = datetime.utcnow()

    # 4. Enregistrer le pointage
    now = datetime.utcnow()
    attendance = _record_biometric_attendance(employee, device, now, event_type, "fingerprint")

    return jsonify({
        "matched": True,
        "employee_id": employee.id,
        "employee_name": f"{employee.first_name} {employee.last_name}",
        "event_type": event_type,
        "timestamp": now.isoformat(),
        "attendance_id": attendance.id if attendance else None,
    })


# -------------------------------------------------------------------
# Attribution & pointage RFID
# -------------------------------------------------------------------

@biometric_bp.post("/rfid/assign")
@jwt_required()
def assign_rfid():
    """
    Associe un code RFID (uid) à un employé.
    Body JSON: { "employee_id": 1, "rfid_uid": "A1B2C3D4" }
    """
    claims = get_jwt()
    perms = claims.get("permissions", [])
    if "manage_biometric_devices" not in perms and "admin_all" not in perms:
        raise AppException("Permission refusée", 403)

    data = request.get_json(force=True)
    employee_id = data.get("employee_id")
    rfid_uid = (data.get("rfid_uid") or "").strip().upper()

    if not employee_id or not rfid_uid:
        raise AppException("employee_id et rfid_uid sont requis", 400)

    # Vérifier qu'une autre carte n'a pas le même UID
    existing = Employee.query.filter_by(rfid_uid=rfid_uid).first()
    if existing and existing.id != employee_id:
        raise AppException(f"Cet UID RFID est déjà attribué à {existing.first_name} {existing.last_name}", 409)

    employee = db.session.get(Employee, employee_id)
    if not employee:
        raise AppException("Employé introuvable", 404)

    employee.rfid_uid = rfid_uid
    db.session.commit()
    return jsonify({
        "message": f"Carte RFID {rfid_uid} attribuée à {employee.first_name} {employee.last_name}",
        "employee_id": employee_id,
        "rfid_uid": rfid_uid,
    })


@biometric_bp.post("/rfid/revoke/<int:employee_id>")
@jwt_required()
def revoke_rfid(employee_id: int):
    """Désactive la carte RFID d'un employé."""
    claims = get_jwt()
    perms = claims.get("permissions", [])
    if "manage_biometric_devices" not in perms and "admin_all" not in perms:
        raise AppException("Permission refusée", 403)

    employee = db.session.get(Employee, employee_id)
    if not employee:
        raise AppException("Employé introuvable", 404)

    employee.rfid_uid = None
    db.session.commit()
    return jsonify({"message": "Carte RFID révoquée"})


@biometric_bp.get("/rfid/lookup/<uid>")
@jwt_required()
def rfid_lookup(uid: str):
    """Identifie un employé à partir de son UID RFID."""
    uid = uid.strip().upper()
    employee = Employee.query.filter_by(rfid_uid=uid).first()
    if not employee:
        return jsonify({"found": False}), 200
    return jsonify({
        "found": True,
        "employee_id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "matricule": employee.matricule,
        "department": employee.department.name if employee.department else None,
        "status": employee.status,
    })


@biometric_bp.post("/rfid/checkin")
@jwt_required()
def rfid_checkin():
    """
    Pointage via carte RFID. Body JSON:
    { "rfid_uid": "A1B2C3D4", "device_id": 1, "event_type": "check_in" | "check_out" }
    """
    data = request.get_json(force=True)
    uid = (data.get("rfid_uid") or "").strip().upper()
    device_id = data.get("device_id")
    event_type = data.get("event_type", "check_in")

    if not uid:
        raise AppException("rfid_uid requis", 400)

    employee = Employee.query.filter_by(rfid_uid=uid).first()
    if not employee:
        return jsonify({"recognized": False, "message": "Carte non reconnue"}), 200

    device = db.session.get(BiometricDevice, device_id) if device_id else None
    if device:
        device.last_seen = datetime.utcnow()

    now = datetime.utcnow()
    attendance = _record_biometric_attendance(employee, device, now, event_type, "rfid")

    return jsonify({
        "recognized": True,
        "employee_id": employee.id,
        "employee_name": f"{employee.first_name} {employee.last_name}",
        "event_type": event_type,
        "timestamp": now.isoformat(),
        "attendance_id": attendance.id if attendance else None,
    })


# -------------------------------------------------------------------
# Pointage biométrique interne (webhook depuis fingerprint-service)
# -------------------------------------------------------------------

@biometric_bp.post("/event")
def biometric_event():
    """
    Endpoint webhook appelé par le fingerprint-service (C#) pour notifier un pointage.
    Ne nécessite pas de JWT — sécurisé par X-DEVICE-TOKEN dans le header.
    Body JSON: { "rfid_uid"?: "...", "employee_id"?: 1, "event_type": "check_in"|"check_out", "device_name": "..." }
    """
    token = request.headers.get("X-DEVICE-TOKEN", "")
    # Vérification minimaliste du token device (hash SHA-256 d'un secret partagé)
    # En production, utiliser un mécanisme de token plus robuste
    expected_hash = hashlib.sha256(b"cnss-biometric-device-shared-secret").hexdigest()
    if not token or token != expected_hash:
        return jsonify({"error": "Non autorisé"}), 401

    data = request.get_json(force=True)
    event_type = data.get("event_type", "check_in")
    rfid_uid = (data.get("rfid_uid") or "").strip().upper()
    employee_id = data.get("employee_id")

    employee = None
    source = "manual"

    if rfid_uid:
        employee = Employee.query.filter_by(rfid_uid=rfid_uid).first()
        source = "rfid"
    elif employee_id:
        employee = db.session.get(Employee, employee_id)
        source = "fingerprint"

    if not employee:
        return jsonify({"success": False, "message": "Employé non identifié"}), 200

    now = datetime.utcnow()
    attendance = _record_biometric_attendance(employee, None, now, event_type, source)

    return jsonify({
        "success": True,
        "employee_id": employee.id,
        "employee_name": f"{employee.first_name} {employee.last_name}",
        "timestamp": now.isoformat(),
        "attendance_id": attendance.id if attendance else None,
    })


# -------------------------------------------------------------------
# Helper interne : enregistrement du pointage
# -------------------------------------------------------------------

def _record_biometric_attendance(
    employee: Employee,
    device: BiometricDevice | None,
    now: datetime,
    event_type: str,
    source: str,
) -> Attendance | None:
    """Crée ou complète un enregistrement de présence biométrique."""
    today = now.date()

    if event_type == "check_in":
        # Vérifier s'il n'y a pas déjà un check-in sans check-out aujourd'hui
        existing = (
            Attendance.query
            .filter_by(employee_id=employee.id)
            .filter(db.func.date(Attendance.check_in) == today)
            .filter(Attendance.check_out.is_(None))
            .first()
        )
        if existing:
            return existing  # Déjà pointé, pas de doublon

        att = Attendance(
            employee_id=employee.id,
            check_in=now,
            biometric_source=source,
            device_id=device.id if device else None,
        )
        db.session.add(att)
        db.session.commit()
        return att

    elif event_type == "check_out":
        # Compléter le dernier check-in sans check-out
        att = (
            Attendance.query
            .filter_by(employee_id=employee.id)
            .filter(db.func.date(Attendance.check_in) == today)
            .filter(Attendance.check_out.is_(None))
            .order_by(Attendance.check_in.desc())
            .first()
        )
        if att:
            att.check_out = now
            delta = (now - att.check_in).total_seconds() / 3600
            att.worked_hours = round(delta, 2)
            att.biometric_source = source
            db.session.commit()
        return att

    return None
