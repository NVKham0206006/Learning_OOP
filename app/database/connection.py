"""
Database connection management and initialization module.
"""

import sqlite3
import os
from typing import Optional, Dict

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app.db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")


class DatabaseConnection:
    """Connection provider for SQLite database."""

    _instances: Dict[str, 'DatabaseConnection'] = {}

    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path

    @classmethod
    def get_instance(cls, db_path: Optional[str] = None) -> 'DatabaseConnection':
        path = db_path or DB_FILE
        if path not in cls._instances:
            cls._instances[path] = DatabaseConnection(path)
        return cls._instances[path]

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_database(self) -> None:
        """Executes schema.sql to create all required tables and seed initial data."""
        if not os.path.exists(SCHEMA_FILE):
            raise FileNotFoundError(f"Schema file not found at: {SCHEMA_FILE}")

        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_script = f.read()

        conn = self.get_connection()
        try:
            conn.executescript(schema_script)
            conn.commit()
        finally:
            conn.close()


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Helper function to obtain a database connection, respecting Flask current_app if present."""
    if db_path is None:
        try:
            from flask import current_app
            if current_app and "DATABASE_PATH" in current_app.config:
                db_path = current_app.config["DATABASE_PATH"]
        except Exception:
            pass
    return DatabaseConnection.get_instance(db_path).get_connection()


def init_db(db_path: Optional[str] = None) -> None:
    """Helper function to initialize database tables."""
    instance = DatabaseConnection.get_instance(db_path)
    instance.init_database()

