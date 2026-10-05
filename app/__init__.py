"""
Flask application factory.

Đây là 'Application Factory Pattern' — pattern chuẩn của Flask,
cho phép tạo nhiều instance app với config khác nhau (dev/test/prod),
rất hữu ích cho testing.
"""
import os
from flask import Flask, session

from app.config import config_by_name
from app.database.connection import init_db


def create_app(config_name: str = None) -> Flask:
    """
    Tạo và cấu hình Flask application.

    Args:
        config_name: 'development' | 'testing' | 'production'
                     Nếu None, đọc từ biến môi trường FLASK_ENV.

    Returns:
        Flask app đã được cấu hình đầy đủ.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    if config_name not in config_by_name:
        raise ValueError(
            f"Config '{config_name}' không hợp lệ. "
            f"Chọn một trong: {list(config_by_name.keys())}"
        )

    app = Flask(__name__)

    # ------------------------------------------------------------------
    # 1. Load config
    # ------------------------------------------------------------------
    app.config.from_object(config_by_name[config_name])

    # Secret key bắt buộc cho session — fallback an toàn cho dev
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"

    # ------------------------------------------------------------------
    # 2. Khởi tạo database (tạo bảng + seed nếu chưa có)
    # ------------------------------------------------------------------
    db_path = app.config.get("DATABASE_PATH", "app.db")
    init_db(db_path)

    # ------------------------------------------------------------------
    # 3. Đăng ký blueprints (controllers)
    # ------------------------------------------------------------------
    _register_blueprints(app)

    # ------------------------------------------------------------------
    # 4. Context processor — inject biến dùng chung vào mọi template
    # ------------------------------------------------------------------
    _register_context_processors(app)

    return app


# ======================================================================
# Helper functions (private — dấu _ ở đầu)
# ======================================================================

def _register_blueprints(app: Flask) -> None:
    """Đăng ký tất cả blueprints (controllers) vào app."""
    # Import bên trong hàm để tránh circular import
    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.course_controller import course_bp
    from app.controllers.consultant_controller import consultant_bp
    from app.controllers.program_controller import program_bp
    from app.controllers.assessment_controller import assessment_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(course_bp, url_prefix="/courses")
    app.register_blueprint(consultant_bp, url_prefix="/consultants")
    app.register_blueprint(program_bp, url_prefix="/programs")
    app.register_blueprint(assessment_bp, url_prefix="/assessment")


def _register_context_processors(app: Flask) -> None:
    """
    Inject các biến dùng chung vào mọi template.
    Ví dụ: current_user, is_logged_in, is_admin.
    """

    @app.context_processor
    def inject_user():
        return {
            "current_user_id": session.get("user_id"),
            "current_username": session.get("username"),
            "current_role": session.get("role"),
            "is_logged_in": "user_id" in session,
        }