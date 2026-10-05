"""
Application entry point.

Chạy: python run.py
Hoặc: flask --app run:app run
"""
import os
from app import create_app

# Chọn config theo biến môi trường (mặc định: development)
config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=(config_name == "development"),
    )