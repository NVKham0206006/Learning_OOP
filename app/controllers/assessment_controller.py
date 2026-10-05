"""Assessment controller — sẽ hoàn thiện ở Task 3."""
from flask import Blueprint

assessment_bp = Blueprint("assessment", __name__)


@assessment_bp.route("/select")
def select():
    return "Assessment selection — sẽ hoàn thiện ở Task 3"