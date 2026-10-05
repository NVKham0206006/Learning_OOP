"""Auth controller — register, login, logout, profile."""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash)
from app.services.user_service import UserService
from app.utils.decorators import login_required

auth_bp = Blueprint("auth", __name__)
user_service = UserService()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip() or None

        if password != confirm:
            flash("Mật khẩu xác nhận không khớp.", "error")
            return render_template("auth/register.html",
                                   form=request.form)

        try:
            user_service.register(username, email, password, full_name, phone)
            flash("Đăng ký thành công! Hãy đăng nhập.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("auth/register.html", form={})


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = user_service.authenticate(username, password)
        if user:
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            session["full_name"] = user.full_name
            session["role"] = user.role
            flash(f"Chào mừng {user.full_name}!", "success")

            # Redirect theo role
            if user.role == "ADMIN":
                return redirect(url_for("admin.dashboard"))
            if user.role == "CONSULTANT":
                return redirect(url_for("consultant.dashboard"))
            return redirect(url_for("home.index"))

        flash("Sai tên đăng nhập hoặc mật khẩu.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Đã đăng xuất.", "info")
    return redirect(url_for("home.index"))


@auth_bp.route("/profile")
@login_required
def profile():
    user = user_service.get_by_id(session["user_id"])
    return render_template("auth/profile.html", user=user)


@auth_bp.route("/profile", methods=["POST"])
@login_required
def update_profile():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip() or None
    try:
        user_service.update_profile(session["user_id"], full_name, email, phone)
        session["full_name"] = full_name
        flash("Cập nhật thông tin thành công.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("auth.profile"))