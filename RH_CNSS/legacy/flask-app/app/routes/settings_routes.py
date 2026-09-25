"""
Rôle du fichier:
Expose les endpoints de paramétrage du système: paramètres, jours fériés, horaires (Module 14).
"""

from datetime import datetime, date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.extensions import db
from app.models import Holiday, SystemParameter
from app.utils.activity_logger import log_activity

settings_bp = Blueprint("settings", __name__)


# ── Paramètres système ────────────────────────────────────────────────────────

@settings_bp.get("/parameters")
@jwt_required()
def list_parameters():
    params = SystemParameter.query.order_by(SystemParameter.key).all()
    return jsonify([_param_dict(p) for p in params])


@settings_bp.get("/parameters/<string:key>")
@jwt_required()
def get_parameter(key):
    param = SystemParameter.query.filter_by(key=key).first_or_404()
    return jsonify(_param_dict(param))


@settings_bp.put("/parameters/<string:key>")
@jwt_required()
def upsert_parameter(key):
    data = request.get_json() or {}
    param = SystemParameter.query.filter_by(key=key).first()
    if param:
        param.value = data.get("value", param.value)
        param.description = data.get("description", param.description)
        param.updated_at = datetime.utcnow()
    else:
        param = SystemParameter(
            key=key,
            value=data.get("value"),
            description=data.get("description"),
        )
        db.session.add(param)
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Paramètre mis à jour: {key}")
    return jsonify(_param_dict(param))


@settings_bp.post("/parameters/bulk")
@jwt_required()
def bulk_upsert_parameters():
    """Mise à jour groupée de plusieurs paramètres."""
    data = request.get_json() or {}
    items = data.get("parameters", [])
    updated = []
    for item in items:
        if not item.get("key"):
            continue
        param = SystemParameter.query.filter_by(key=item["key"]).first()
        if param:
            param.value = item.get("value", param.value)
            param.updated_at = datetime.utcnow()
        else:
            param = SystemParameter(key=item["key"], value=item.get("value"), description=item.get("description"))
            db.session.add(param)
        updated.append(item["key"])
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Paramètres mis à jour en masse: {', '.join(updated)}")
    return jsonify({"updated": updated})


# ── Jours fériés ──────────────────────────────────────────────────────────────

@settings_bp.get("/holidays")
@jwt_required()
def list_holidays():
    holidays = Holiday.query.order_by(Holiday.date).all()
    return jsonify([_holiday_dict(h) for h in holidays])


@settings_bp.post("/holidays")
@jwt_required()
def create_holiday():
    data = request.get_json() or {}
    if not data.get("name") or not data.get("date"):
        return jsonify({"error": "name et date requis"}), 400
    h = Holiday(
        name=data["name"],
        date=date.fromisoformat(data["date"]),
        is_recurring=data.get("is_recurring", False),
    )
    db.session.add(h)
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Jour férié créé: {h.name}")
    return jsonify(_holiday_dict(h)), 201


@settings_bp.put("/holidays/<int:holiday_id>")
@jwt_required()
def update_holiday(holiday_id):
    h = Holiday.query.get_or_404(holiday_id)
    data = request.get_json() or {}
    if "name" in data:
        h.name = data["name"]
    if "date" in data:
        h.date = date.fromisoformat(data["date"])
    if "is_recurring" in data:
        h.is_recurring = data["is_recurring"]
    db.session.commit()
    return jsonify(_holiday_dict(h))


@settings_bp.delete("/holidays/<int:holiday_id>")
@jwt_required()
def delete_holiday(holiday_id):
    h = Holiday.query.get_or_404(holiday_id)
    db.session.delete(h)
    db.session.commit()
    return jsonify({"message": "Jour férié supprimé"})


# ── Helpers ───────────────────────────────────────────────────────────────────

def _param_dict(p: SystemParameter) -> dict:
    return {
        "id": p.id,
        "key": p.key,
        "value": p.value,
        "description": p.description,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }


def _holiday_dict(h: Holiday) -> dict:
    return {
        "id": h.id,
        "name": h.name,
        "date": h.date.isoformat() if h.date else None,
        "is_recurring": h.is_recurring,
        "created_at": h.created_at.isoformat() if h.created_at else None,
    }
