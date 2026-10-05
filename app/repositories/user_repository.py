from typing import Optional, List
from .base_repository import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    """Data access repository for User entities."""

    def get_by_id(self, entity_id: int) -> Optional[User]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                password_hash=row["password_hash"],
                full_name=row["full_name"],
                role=row["role"],
                phone=row["phone"],
                is_active=bool(row["is_active"])
            )
        finally:
            conn.close()

    def get_by_username(self, username: str) -> Optional[User]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
            row = cursor.fetchone()
            if not row:
                return None
            return User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                password_hash=row["password_hash"],
                full_name=row["full_name"],
                role=row["role"],
                phone=row["phone"],
                is_active=bool(row["is_active"])
            )
        finally:
            conn.close()

    def get_by_email(self, email: str) -> Optional[User]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
            row = cursor.fetchone()
            if not row:
                return None
            return User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                password_hash=row["password_hash"],
                full_name=row["full_name"],
                role=row["role"],
                phone=row["phone"],
                is_active=bool(row["is_active"])
            )
        finally:
            conn.close()

    def get_all(self) -> List[User]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY id ASC")
            rows = cursor.fetchall()
            return [
                User(
                    id=r["id"],
                    username=r["username"],
                    email=r["email"],
                    password_hash=r["password_hash"],
                    full_name=r["full_name"],
                    role=r["role"],
                    phone=r["phone"],
                    is_active=bool(r["is_active"])
                )
                for r in rows
            ]
        finally:
            conn.close()

    def get_all_by_role(self, role: str) -> List[User]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE UPPER(role) = UPPER(?) ORDER BY id ASC", (role,))
            rows = cursor.fetchall()
            return [
                User(
                    id=r["id"],
                    username=r["username"],
                    email=r["email"],
                    password_hash=r["password_hash"],
                    full_name=r["full_name"],
                    role=r["role"],
                    phone=r["phone"],
                    is_active=bool(r["is_active"])
                )
                for r in rows
            ]
        finally:
            conn.close()

    def create(self, user: User) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash, full_name, role, phone, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user.username, user.email, user.password_hash, user.full_name, user.role, user.phone, int(user.is_active))
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_profile(self, user_id: int, full_name: str, email: str, phone: Optional[str]) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users
                SET full_name = ?, email = ?, phone = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (full_name, email, phone, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

