"""Home controller — trang chủ."""
from flask import Blueprint, render_template
from app.services.course_service import CourseService
from app.services.consultant_service import ConsultantService

home_bp = Blueprint("home", __name__)
course_service = CourseService()
consultant_service = ConsultantService()


@home_bp.route("/")
def index():
    """Trang chủ hiển thị top courses + consultants."""
    courses = course_service.list_published()[:4]
    consultants = consultant_service.list_all()[:2]
    return render_template("index.html", courses=courses, consultants=consultants)


@home_bp.route("/about")
def about():
    return render_template("about.html")


@home_bp.route("/blog")
def blog_list():
    return render_template("blog/list.html")