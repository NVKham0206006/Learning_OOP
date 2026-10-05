def _register_blueprints(app):
    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.course_controller import course_bp
    from app.controllers.consultant_controller import consultant_bp
    from app.controllers.program_controller import program_bp
    from app.controllers.assessment_controller import assessment_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.admin_controller import admin_bp  # ← Tạo ở dưới

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(course_bp, url_prefix="/courses")
    app.register_blueprint(consultant_bp, url_prefix="/consultants")
    app.register_blueprint(program_bp, url_prefix="/programs")
    app.register_blueprint(assessment_bp, url_prefix="/assessment")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")