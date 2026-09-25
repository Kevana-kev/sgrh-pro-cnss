"""
Rôle du fichier:
Enregistre tous les blueprints Flask et connecte les routes API à l'application.
"""

from flask import Flask

from app.routes.account_routes import account_bp
from app.routes.attendance_routes import attendance_bp
from app.routes.auth_routes import auth_bp
from app.routes.biometric_routes import biometric_bp
from app.routes.contract_routes import contract_bp
from app.routes.department_routes import department_bp
from app.routes.employee_routes import employee_bp
from app.routes.leave_routes import leave_bp
from app.routes.medical_leave_routes import medical_leave_bp
from app.routes.message_routes import message_bp
from app.routes.notification_routes import notification_bp
from app.routes.payroll_routes import payroll_bp
from app.routes.performance_routes import performance_bp
from app.routes.recruitment_routes import recruitment_bp
from app.routes.report_routes import report_bp
from app.routes.role_routes import role_bp
from app.routes.settings_routes import settings_bp
from app.routes.training_routes import training_bp
from app.routes.ui_routes import ui_bp


def register_blueprints(app: Flask) -> None:
    """Enregistre tous les blueprints API et UI sur l'application Flask."""
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(account_bp, url_prefix="/api/accounts")
    app.register_blueprint(employee_bp, url_prefix="/api/employees")
    app.register_blueprint(department_bp, url_prefix="/api/departments")
    app.register_blueprint(role_bp, url_prefix="/api/roles")
    app.register_blueprint(payroll_bp, url_prefix="/api/payrolls")
    app.register_blueprint(attendance_bp, url_prefix="/api/attendances")
    app.register_blueprint(leave_bp, url_prefix="/api/leaves")
    app.register_blueprint(contract_bp, url_prefix="/api/contracts")
    app.register_blueprint(report_bp, url_prefix="/api/reports")
    app.register_blueprint(message_bp, url_prefix="/api/messages")
    app.register_blueprint(biometric_bp, url_prefix="/api/biometric")
    app.register_blueprint(training_bp, url_prefix="/api/trainings")
    app.register_blueprint(performance_bp, url_prefix="/api/evaluations")
    app.register_blueprint(medical_leave_bp, url_prefix="/api/medical-leaves")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")
    app.register_blueprint(recruitment_bp, url_prefix="/api/recruitment")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(ui_bp)
