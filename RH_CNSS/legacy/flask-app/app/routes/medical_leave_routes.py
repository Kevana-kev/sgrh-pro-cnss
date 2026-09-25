"""
Rôle du fichier:
Expose les endpoints de gestion des congés médicaux et arrêts maladie (Module 10).
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models import MedicalLeave, User
from app.utils.activity_logger import log_activity

medical_leave_bp = Blueprint("medical_leaves", __name__)


@medical_leave_bp.get("")
@jwt_required()
def list_medical_leaves():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if claims.get("role") in ("Administrateur", "RH") or "Voir congés médicaux" in (claims.get("permissions") or []):
        leaves = MedicalLeave.query.order_by(MedicalLeave.created_at.desc()).all()
    else:
        emp_id = user.employee_id if user else None
        leaves = MedicalLeave.query.filter_by(employee_id=emp_id).all() if emp_id else []
    return jsonify([_ml_dict(ml) for ml in leaves])


@medical_leave_bp.post("")
@jwt_required()
def create_medical_leave():
    data = request.get_json() or {}
    required = ["employee_id", "start_date", "end_date"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"Champ requis: {f}"}), 400
    from datetime import date
    ml = MedicalLeave(
        employee_id=data["employee_id"],
        start_date=date.fromisoformat(data["start_date"]),
        end_date=date.fromisoformat(data["end_date"]),
        diagnosis=data.get("diagnosis"),
        certificate_path=data.get("certificate_path"),
        daily_allowance=data.get("daily_allowance", 0.0),
        status=data.get("status", "En attente"),
    )
    db.session.add(ml)
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Congé médical #{ml.id} créé")
    return jsonify(_ml_dict(ml)), 201


@medical_leave_bp.get("/<int:ml_id>")
@jwt_required()
def get_medical_leave(ml_id):
    ml = MedicalLeave.query.get_or_404(ml_id)
    return jsonify(_ml_dict(ml))


@medical_leave_bp.put("/<int:ml_id>")
@jwt_required()
def update_medical_leave(ml_id):
    ml = MedicalLeave.query.get_or_404(ml_id)
    data = request.get_json() or {}
    for field in ["diagnosis", "certificate_path", "daily_allowance", "status"]:
        if field in data:
            setattr(ml, field, data[field])
    from datetime import date
    if "start_date" in data:
        ml.start_date = date.fromisoformat(data["start_date"])
    if "end_date" in data:
        ml.end_date = date.fromisoformat(data["end_date"])
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Congé médical #{ml_id} mis à jour")
    return jsonify(_ml_dict(ml))


@medical_leave_bp.delete("/<int:ml_id>")
@jwt_required()
def delete_medical_leave(ml_id):
    ml = MedicalLeave.query.get_or_404(ml_id)
    db.session.delete(ml)
    db.session.commit()
    return jsonify({"message": "Congé médical supprimé"})


def _ml_dict(ml: MedicalLeave) -> dict:
    emp = ml.employee
    return {
        "id": ml.id,
        "employee_id": ml.employee_id,
        "employee_name": f"{emp.first_name} {emp.last_name}" if emp else None,
        "start_date": ml.start_date.isoformat() if ml.start_date else None,
        "end_date": ml.end_date.isoformat() if ml.end_date else None,
        "diagnosis": ml.diagnosis,
        "certificate_path": ml.certificate_path,
        "daily_allowance": ml.daily_allowance,
        "status": ml.status,
        "created_at": ml.created_at.isoformat() if ml.created_at else None,
    }
