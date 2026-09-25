"""
Rôle du fichier:
Expose les endpoints de gestion des notifications et alertes système (Module 11).
"""

from datetime import datetime, date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Contract, Employee, Leave, Notification, User
from app.utils.activity_logger import log_activity

notification_bp = Blueprint("notifications", __name__)


@notification_bp.get("")
@jwt_required()
def list_notifications():
    """Retourne les notifications de l'utilisateur courant (+ broadcast)."""
    user_id = int(get_jwt_identity())
    notifs = Notification.query.filter(
        (Notification.user_id == user_id) | (Notification.user_id.is_(None))
    ).order_by(Notification.created_at.desc()).limit(50).all()
    return jsonify([_notif_dict(n) for n in notifs])


@notification_bp.get("/unread-count")
@jwt_required()
def unread_count():
    user_id = int(get_jwt_identity())
    count = Notification.query.filter(
        ((Notification.user_id == user_id) | (Notification.user_id.is_(None))),
        Notification.is_read == False,
    ).count()
    return jsonify({"count": count})


@notification_bp.put("/<int:notif_id>/read")
@jwt_required()
def mark_read(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    notif.is_read = True
    db.session.commit()
    return jsonify({"message": "Marquée comme lue"})


@notification_bp.put("/read-all")
@jwt_required()
def mark_all_read():
    user_id = int(get_jwt_identity())
    Notification.query.filter(
        (Notification.user_id == user_id) | (Notification.user_id.is_(None))
    ).update({"is_read": True})
    db.session.commit()
    return jsonify({"message": "Toutes marquées comme lues"})


@notification_bp.post("")
@jwt_required()
def create_notification():
    """Crée une notification manuellement (admin/RH)."""
    data = request.get_json() or {}
    if not data.get("title") or not data.get("message"):
        return jsonify({"error": "title et message requis"}), 400
    notif = Notification(
        user_id=data.get("user_id"),
        type=data.get("type", "info"),
        title=data["title"],
        message=data["message"],
    )
    db.session.add(notif)
    db.session.commit()
    return jsonify(_notif_dict(notif)), 201


@notification_bp.delete("/<int:notif_id>")
@jwt_required()
def delete_notification(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    db.session.delete(notif)
    db.session.commit()
    return jsonify({"message": "Notification supprimée"})


@notification_bp.post("/generate-alerts")
@jwt_required()
def generate_alerts():
    """Génère automatiquement des alertes: fins de contrat, anniversaires, congés en attente."""
    today = date.today()
    created = 0

    # Contrats qui expirent dans 30 jours
    from datetime import timedelta
    in_30 = today + timedelta(days=30)
    contracts_expiring = Contract.query.filter(
        Contract.end_date != None,
        Contract.end_date >= today,
        Contract.end_date <= in_30,
    ).all()
    for c in contracts_expiring:
        emp = c.employee
        exists = Notification.query.filter_by(
            type="contract_expiry",
            title=f"Contrat expirant bientôt — {emp.first_name} {emp.last_name}",
        ).filter(Notification.created_at >= datetime.utcnow().replace(hour=0, minute=0)).first()
        if not exists:
            n = Notification(
                type="contract_expiry",
                title=f"Contrat expirant bientôt — {emp.first_name} {emp.last_name}",
                message=f"Le contrat de {emp.first_name} {emp.last_name} expire le {c.end_date}.",
            )
            db.session.add(n)
            created += 1

    # Congés en attente depuis plus de 3 jours
    from app.models import Leave
    pending_leaves = Leave.query.filter_by(status="En attente").all()
    for lv in pending_leaves:
        age = (datetime.utcnow().date() - lv.start_date).days if hasattr(lv, 'start_date') else 0
        if age > 3:
            exists = Notification.query.filter_by(
                type="leave_pending",
                title=f"Congé en attente — Employé #{lv.employee_id}",
            ).filter(Notification.created_at >= datetime.utcnow().replace(hour=0, minute=0)).first()
            if not exists:
                n = Notification(
                    type="leave_pending",
                    title=f"Congé en attente — Employé #{lv.employee_id}",
                    message=f"Une demande de congé est en attente depuis plus de 3 jours.",
                )
                db.session.add(n)
                created += 1

    db.session.commit()
    return jsonify({"message": f"{created} alerte(s) générée(s)"})


def _notif_dict(n: Notification) -> dict:
    return {
        "id": n.id,
        "user_id": n.user_id,
        "type": n.type,
        "title": n.title,
        "message": n.message,
        "is_read": n.is_read,
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }
