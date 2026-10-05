"""Community program controller."""
from flask import Blueprint

program_bp = Blueprint("program", __name__)


@program_bp.route("/")
def list_programs():
    return "Programs list — sẽ hoàn thiện ở Task 4"