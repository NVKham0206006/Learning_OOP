"""Course controller — list, detail, enroll, my-courses."""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash)
from app.services.course_service import CourseService
from app.utils.decorators import login_required

course_bp = Blueprint("course", __name__)
course_service = CourseService()


@course_bp.route("/")
def list_courses():
    keyword = request.args.get("q", "").strip()
    courses = course_service.search(keyword)
    return render_template("course/list.html", courses=courses, keyword=keyword)


@course_bp.route("/<int:course_id>")
def detail(course_id):
    course = course_service.get_by_id(course_id)
    if not course:
        flash("Khóa học không tồn tại.", "error")
        return redirect(url_for("course.list_courses"))
    lessons = course_service.get_lessons(course_id)
    is_enrolled = False
    if "user_id" in session:
        enrollments = course_service.get_user_enrollments(session["user_id"])
        is_enrolled = any(e.course_id == course_id for e in enrollments)
    return render_template("course/detail.html",
                           course=course, lessons=lessons, is_enrolled=is_enrolled)


@course_bp.route("/<int:course_id>/enroll", methods=["POST"])
@login_required
def enroll(course_id):
    try:
        course_service.enroll(session["user_id"], course_id)
        flash("Đăng ký khóa học thành công!", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("course.detail", course_id=course_id))


@course_bp.route("/my-courses")
@login_required
def my_courses():
    enrollments = course_service.get_user_enrollments(session["user_id"])
    return render_template("course/my_courses.html", enrollments=enrollments)