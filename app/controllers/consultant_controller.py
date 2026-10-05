"""Consultant controller — list, detail."""
from flask import Blueprint, render_template, flash, redirect, url_for
from app.services.consultant_service import ConsultantService

consultant_bp = Blueprint("consultant", __name__)
consultant_service = ConsultantService()


@consultant_bp.route("/")
def list_consultants():
    keyword = ""
    from flask import request
    keyword = request.args.get("q", "").strip()
    consultants = consultant_service.search(keyword)
    return render_template("consultant/list.html",
                           consultants=consultants, keyword=keyword)


@consultant_bp.route("/<int:consultant_id>")
def detail(consultant_id):
    consultant = consultant_service.get_by_id(consultant_id)
    if not consultant:
        flash("Không tìm thấy chuyên gia.", "error")
        return redirect(url_for("consultant.list_consultants"))
    schedules = consultant_service.get_schedules(consultant_id)
    return render_template("consultant/detail.html",
                           consultant=consultant, schedules=schedules)


@consultant_bp.route("/dashboard")
def dashboard():
    from app.controllers.dashboard_controller import consultant_dashboard
    return consultant_dashboard()