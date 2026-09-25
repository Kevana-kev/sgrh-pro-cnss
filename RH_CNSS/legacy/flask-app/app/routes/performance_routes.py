"""
Rôle du fichier:
Expose les endpoints de gestion des évaluations de performance (Module 9).
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Employee, PerformanceEvaluation, User
from app.utils.activity_logger import log_activity

performance_bp = Blueprint("performance", __name__)


@performance_bp.get("")
@jwt_required()
def list_evaluations():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if "Voir évaluations" in (claims.get("permissions") or []) or claims.get("role") in ("Administrateur", "RH"):
        evals = PerformanceEvaluation.query.order_by(PerformanceEvaluation.created_at.desc()).all()
    else:
        emp_id = user.employee_id if user else None
        evals = PerformanceEvaluation.query.filter_by(employee_id=emp_id).all() if emp_id else []
    return jsonify([_eval_dict(e) for e in evals])


@performance_bp.post("")
@jwt_required()
def create_evaluation():
    data = request.get_json() or {}
    required = ["employee_id", "period"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"Champ requis: {f}"}), 400
    ev = PerformanceEvaluation(
        employee_id=data["employee_id"],
        evaluator_id=data.get("evaluator_id"),
        period=data["period"],
        score=data.get("score"),
        objectives=data.get("objectives"),
        comments=data.get("comments"),
        status=data.get("status", "en cours"),
    )
    db.session.add(ev)
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Évaluation créée employé #{ev.employee_id}")
    return jsonify(_eval_dict(ev)), 201


@performance_bp.get("/<int:eval_id>")
@jwt_required()
def get_evaluation(eval_id):
    ev = PerformanceEvaluation.query.get_or_404(eval_id)
    return jsonify(_eval_dict(ev))


@performance_bp.put("/<int:eval_id>")
@jwt_required()
def update_evaluation(eval_id):
    ev = PerformanceEvaluation.query.get_or_404(eval_id)
    data = request.get_json() or {}
    for field in ["period", "score", "objectives", "comments", "status"]:
        if field in data:
            setattr(ev, field, data[field])
    db.session.commit()
    return jsonify(_eval_dict(ev))


@performance_bp.delete("/<int:eval_id>")
@jwt_required()
def delete_evaluation(eval_id):
    ev = PerformanceEvaluation.query.get_or_404(eval_id)
    db.session.delete(ev)
    db.session.commit()
    return jsonify({"message": "Évaluation supprimée"})


@performance_bp.get("/stats")
@jwt_required()
def evaluation_stats():
    """Statistiques d'évaluation: moyennes par département, distribution des scores."""
    evals = PerformanceEvaluation.query.filter(PerformanceEvaluation.score.isnot(None)).all()
    if not evals:
        return jsonify({"avg_score": 0, "total": 0, "by_status": {}})
    avg = sum(e.score for e in evals) / len(evals)
    by_status = {}
    for e in PerformanceEvaluation.query.all():
        by_status[e.status] = by_status.get(e.status, 0) + 1
    return jsonify({
        "avg_score": round(avg, 2),
        "total": PerformanceEvaluation.query.count(),
        "by_status": by_status,
    })


def _eval_dict(ev: PerformanceEvaluation) -> dict:
    emp = ev.employee
    evaluator = ev.evaluator
    return {
        "id": ev.id,
        "employee_id": ev.employee_id,
        "employee_name": f"{emp.first_name} {emp.last_name}" if emp else None,
        "evaluator_id": ev.evaluator_id,
        "evaluator_name": f"{evaluator.first_name} {evaluator.last_name}" if evaluator else None,
        "period": ev.period,
        "score": ev.score,
        "objectives": ev.objectives,
        "comments": ev.comments,
        "status": ev.status,
        "created_at": ev.created_at.isoformat() if ev.created_at else None,
    }
