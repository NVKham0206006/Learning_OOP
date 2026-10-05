"""Dashboard controller — trang riêng theo role."""
from flask import Blueprint, render_template, session
from app.utils.decorators import login_required, role_required
from app.services.user_service import UserService
from app.services.course_service import CourseService
from app.services.consultant_service import ConsultantService

dashboard_bp = Blueprint("dashboard", __name__)
user_service = UserService()
course_service = CourseService()
consultant_service = ConsultantService()


@dashboard_bp.route("/user")
@login_required
def user_dashboard():
    user = user_service.get_by_id(session["user_id"])
    enrollments = course_service.get_user_enrollments(session["user_id"])
    return render_template("dashboard/user.html", user=user, enrollments=enrollments)


@dashboard_bp.route("/consultant")
@role_required("CONSULTANT")
def consultant_dashboard():
    consultant = consultant_service.get_by_user_id(session["user_id"])
    schedules = consultant_service.get_schedules(consultant.id) if consultant else []
    return render_template("dashboard/consultant.html",
                           consultant=consultant, schedules=schedules)


@dashboard_bp.route("/admin")
@role_required("ADMIN")
def admin_dashboard():
    users = user_service.list_all()
    consultants = consultant_service.list_all()
    courses = course_service.admin_list_all()
    return render_template("dashboard/admin.html",
                           users=users, consultants=consultants, courses=courses)