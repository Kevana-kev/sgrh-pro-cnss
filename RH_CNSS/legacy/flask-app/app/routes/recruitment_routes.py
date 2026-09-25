"""
Rôle du fichier:
Expose les endpoints de gestion du recrutement: offres d'emploi et candidatures (Module 12).
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.extensions import db
from app.models import Department, JobApplication, JobOffer
from app.utils.activity_logger import log_activity

recruitment_bp = Blueprint("recruitment", __name__)


# ── Offres d'emploi ───────────────────────────────────────────────────────────

@recruitment_bp.get("/offers")
@jwt_required()
def list_offers():
    offers = JobOffer.query.order_by(JobOffer.created_at.desc()).all()
    return jsonify([_offer_dict(o) for o in offers])


@recruitment_bp.post("/offers")
@jwt_required()
def create_offer():
    data = request.get_json() or {}
    if not data.get("title"):
        return jsonify({"error": "title requis"}), 400
    offer = JobOffer(
        title=data["title"],
        department_id=data.get("department_id"),
        description=data.get("description"),
        requirements=data.get("requirements"),
        status=data.get("status", "ouvert"),
    )
    db.session.add(offer)
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Offre recrutement créée: {offer.title}")
    return jsonify(_offer_dict(offer)), 201


@recruitment_bp.get("/offers/<int:offer_id>")
@jwt_required()
def get_offer(offer_id):
    offer = JobOffer.query.get_or_404(offer_id)
    result = _offer_dict(offer)
    result["applications"] = [_application_dict(a) for a in offer.applications]
    return jsonify(result)


@recruitment_bp.put("/offers/<int:offer_id>")
@jwt_required()
def update_offer(offer_id):
    offer = JobOffer.query.get_or_404(offer_id)
    data = request.get_json() or {}
    for field in ["title", "description", "requirements", "status", "department_id"]:
        if field in data:
            setattr(offer, field, data[field])
    db.session.commit()
    return jsonify(_offer_dict(offer))


@recruitment_bp.delete("/offers/<int:offer_id>")
@jwt_required()
def delete_offer(offer_id):
    offer = JobOffer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    return jsonify({"message": "Offre supprimée"})


# ── Candidatures ──────────────────────────────────────────────────────────────

@recruitment_bp.get("/applications")
@jwt_required()
def list_applications():
    apps = JobApplication.query.order_by(JobApplication.created_at.desc()).all()
    return jsonify([_application_dict(a) for a in apps])


@recruitment_bp.post("/offers/<int:offer_id>/applications")
@jwt_required()
def submit_application(offer_id):
    JobOffer.query.get_or_404(offer_id)
    data = request.get_json() or {}
    required = ["applicant_name", "applicant_email"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"Champ requis: {f}"}), 400
    app_obj = JobApplication(
        job_offer_id=offer_id,
        applicant_name=data["applicant_name"],
        applicant_email=data["applicant_email"],
        cv_path=data.get("cv_path"),
        status=data.get("status", "reçu"),
        notes=data.get("notes"),
    )
    if data.get("interview_date"):
        from datetime import datetime
        app_obj.interview_date = datetime.fromisoformat(data["interview_date"])
    db.session.add(app_obj)
    db.session.commit()
    claims = get_jwt()
    log_activity(claims.get("username", "unknown"), f"Candidature reçue: {app_obj.applicant_name}")
    return jsonify(_application_dict(app_obj)), 201


@recruitment_bp.put("/applications/<int:app_id>")
@jwt_required()
def update_application(app_id):
    app_obj = JobApplication.query.get_or_404(app_id)
    data = request.get_json() or {}
    for field in ["status", "notes", "cv_path"]:
        if field in data:
            setattr(app_obj, field, data[field])
    if data.get("interview_date"):
        from datetime import datetime
        app_obj.interview_date = datetime.fromisoformat(data["interview_date"])
    db.session.commit()
    return jsonify(_application_dict(app_obj))


@recruitment_bp.delete("/applications/<int:app_id>")
@jwt_required()
def delete_application(app_id):
    app_obj = JobApplication.query.get_or_404(app_id)
    db.session.delete(app_obj)
    db.session.commit()
    return jsonify({"message": "Candidature supprimée"})


@recruitment_bp.get("/stats")
@jwt_required()
def recruitment_stats():
    total_offers = JobOffer.query.count()
    open_offers = JobOffer.query.filter_by(status="ouvert").count()
    total_apps = JobApplication.query.count()
    by_status = {}
    for a in JobApplication.query.all():
        by_status[a.status] = by_status.get(a.status, 0) + 1
    return jsonify({
        "total_offers": total_offers,
        "open_offers": open_offers,
        "total_applications": total_apps,
        "by_status": by_status,
    })


# ── Helpers ───────────────────────────────────────────────────────────────────

def _offer_dict(o: JobOffer) -> dict:
    return {
        "id": o.id,
        "title": o.title,
        "department_id": o.department_id,
        "department_name": o.department.name if o.department else None,
        "description": o.description,
        "requirements": o.requirements,
        "status": o.status,
        "application_count": len(o.applications) if o.applications else 0,
        "created_at": o.created_at.isoformat() if o.created_at else None,
    }


def _application_dict(a: JobApplication) -> dict:
    return {
        "id": a.id,
        "job_offer_id": a.job_offer_id,
        "offer_title": a.job_offer.title if a.job_offer else None,
        "applicant_name": a.applicant_name,
        "applicant_email": a.applicant_email,
        "cv_path": a.cv_path,
        "status": a.status,
        "interview_date": a.interview_date.isoformat() if a.interview_date else None,
        "notes": a.notes,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }
