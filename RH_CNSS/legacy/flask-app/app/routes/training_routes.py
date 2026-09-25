"""
Rôle du fichier:
Expose les endpoints de gestion des formations et des compétences (Module 8).
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.extensions import db
from app.models import Employee, EmployeeSkill, Skill, Training, TrainingEnrollment
from app.utils.activity_logger import log_activity

training_bp = Blueprint("trainings", __name__)


# ── Formations ────────────────────────────────────────────────────────────────

@training_bp.get("")
@jwt_required()
def list_trainings():
    trainings = Training.query.order_by(Training.start_date.desc()).all()
    return jsonify([_training_dict(t) for t in trainings])


@training_bp.post("")
@jwt_required()
def create_training():
    data = request.get_json() or {}
    required = ["title", "start_date", "end_date"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Champ requis: {field}"}), 400
    from datetime import date
    t = Training(
        title=data["title"],
        description=data.get("description"),
        trainer=data.get("trainer"),
        start_date=date.fromisoformat(data["start_date"]),
        end_date=date.fromisoformat(data["end_date"]),
        max_participants=data.get("max_participants", 20),
        status=data.get("status", "planifié"),
    )
    db.session.add(t)
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Formation créée: {t.title}")
    return jsonify(_training_dict(t)), 201


@training_bp.get("/<int:training_id>")
@jwt_required()
def get_training(training_id):
    t = Training.query.get_or_404(training_id)
    result = _training_dict(t)
    result["enrollments"] = [_enrollment_dict(e) for e in t.enrollments]
    return jsonify(result)


@training_bp.put("/<int:training_id>")
@jwt_required()
def update_training(training_id):
    t = Training.query.get_or_404(training_id)
    data = request.get_json() or {}
    for field in ["title", "description", "trainer", "max_participants", "status"]:
        if field in data:
            setattr(t, field, data[field])
    from datetime import date
    if "start_date" in data:
        t.start_date = date.fromisoformat(data["start_date"])
    if "end_date" in data:
        t.end_date = date.fromisoformat(data["end_date"])
    db.session.commit()
    return jsonify(_training_dict(t))


@training_bp.delete("/<int:training_id>")
@jwt_required()
def delete_training(training_id):
    t = Training.query.get_or_404(training_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Formation supprimée"})


# ── Inscriptions ──────────────────────────────────────────────────────────────

@training_bp.post("/<int:training_id>/enroll")
@jwt_required()
def enroll_employee(training_id):
    Training.query.get_or_404(training_id)
    data = request.get_json() or {}
    employee_id = data.get("employee_id")
    if not employee_id:
        return jsonify({"error": "employee_id requis"}), 400
    existing = TrainingEnrollment.query.filter_by(
        training_id=training_id, employee_id=employee_id
    ).first()
    if existing:
        return jsonify({"error": "Déjà inscrit"}), 409
    enr = TrainingEnrollment(training_id=training_id, employee_id=employee_id)
    db.session.add(enr)
    db.session.commit()
    return jsonify(_enrollment_dict(enr)), 201


@training_bp.put("/enrollments/<int:enrollment_id>")
@jwt_required()
def update_enrollment(enrollment_id):
    enr = TrainingEnrollment.query.get_or_404(enrollment_id)
    data = request.get_json() or {}
    if "status" in data:
        enr.status = data["status"]
    if "score" in data:
        enr.score = data["score"]
    db.session.commit()
    return jsonify(_enrollment_dict(enr))


# ── Compétences ───────────────────────────────────────────────────────────────

@training_bp.get("/skills")
@jwt_required()
def list_skills():
    skills = Skill.query.order_by(Skill.category, Skill.name).all()
    return jsonify([{"id": s.id, "name": s.name, "category": s.category} for s in skills])


@training_bp.post("/skills")
@jwt_required()
def create_skill():
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"error": "name requis"}), 400
    s = Skill(name=data["name"], category=data.get("category"))
    db.session.add(s)
    db.session.commit()
    return jsonify({"id": s.id, "name": s.name, "category": s.category}), 201


@training_bp.get("/employees/<int:employee_id>/skills")
@jwt_required()
def employee_skills(employee_id):
    Employee.query.get_or_404(employee_id)
    skills = EmployeeSkill.query.filter_by(employee_id=employee_id).all()
    return jsonify([_emp_skill_dict(es) for es in skills])


@training_bp.post("/employees/<int:employee_id>/skills")
@jwt_required()
def add_employee_skill(employee_id):
    Employee.query.get_or_404(employee_id)
    data = request.get_json() or {}
    skill_id = data.get("skill_id")
    if not skill_id:
        return jsonify({"error": "skill_id requis"}), 400
    es = EmployeeSkill.query.filter_by(employee_id=employee_id, skill_id=skill_id).first()
    if es:
        es.level = data.get("level", es.level)
    else:
        from datetime import date
        certified = date.fromisoformat(data["certified_at"]) if data.get("certified_at") else None
        es = EmployeeSkill(
            employee_id=employee_id,
            skill_id=skill_id,
            level=data.get("level", 1),
            certified_at=certified,
        )
        db.session.add(es)
    db.session.commit()
    return jsonify(_emp_skill_dict(es)), 201


# ── Helpers ───────────────────────────────────────────────────────────────────

def _training_dict(t: Training) -> dict:
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "trainer": t.trainer,
        "start_date": t.start_date.isoformat() if t.start_date else None,
        "end_date": t.end_date.isoformat() if t.end_date else None,
        "max_participants": t.max_participants,
        "status": t.status,
        "enrolled_count": len(t.enrollments) if t.enrollments else 0,
        "created_at": t.created_at.isoformat() if t.created_at else None,
    }


def _enrollment_dict(e: TrainingEnrollment) -> dict:
    return {
        "id": e.id,
        "training_id": e.training_id,
        "employee_id": e.employee_id,
        "employee_name": f"{e.employee.first_name} {e.employee.last_name}" if e.employee else None,
        "status": e.status,
        "score": e.score,
        "enrolled_at": e.enrolled_at.isoformat() if e.enrolled_at else None,
    }


def _emp_skill_dict(es: EmployeeSkill) -> dict:
    return {
        "id": es.id,
        "employee_id": es.employee_id,
        "skill_id": es.skill_id,
        "skill_name": es.skill.name if es.skill else None,
        "category": es.skill.category if es.skill else None,
        "level": es.level,
        "certified_at": es.certified_at.isoformat() if es.certified_at else None,
    }
