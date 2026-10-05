"""Consultant repository — data access cho Consultant."""
from typing import Optional, List
from app.repositories.base_repository import BaseRepository
from app.models.consultant import Consultant


class ConsultantRepository(BaseRepository[Consultant]):
    """Repository cho entity Consultant."""

    def get_by_id(self, entity_id: int) -> Optional[Consultant]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, u.username, u.email, u.full_name, u.phone AS user_phone
                FROM consultants c
                JOIN users u ON u.id = c.user_id
                WHERE c.id = ?
            """, (entity_id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            conn.close()

    def get_all(self) -> List[Consultant]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, u.username, u.email, u.full_name, u.phone AS user_phone
                FROM consultants c
                JOIN users u ON u.id = c.user_id
                ORDER BY u.full_name ASC
            """)
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_by_user_id(self, user_id: int) -> Optional[Consultant]:
        """Tìm consultant theo user_id."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, u.username, u.email, u.full_name, u.phone AS user_phone
                FROM consultants c
                JOIN users u ON u.id = c.user_id
                WHERE c.user_id = ?
            """, (user_id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            conn.close()

    def search_by_expertise(self, keyword: str) -> List[Consultant]:
        """Tìm consultant theo chuyên môn."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, u.username, u.email, u.full_name, u.phone AS user_phone
                FROM consultants c
                JOIN users u ON u.id = c.user_id
                WHERE LOWER(c.expertise) LIKE LOWER(?)
                ORDER BY u.full_name ASC
            """, (f"%{keyword}%",))
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def create(self, consultant: Consultant) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO consultants (user_id, expertise, bio, phone)
                VALUES (?, ?, ?, ?)
            """, (consultant.user_id, consultant.expertise,
                  consultant.bio, consultant.phone))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_expertise(self, consultant_id: int, qualifications: str, bio: str,
                         years_of_experience: int = None) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if years_of_experience is not None:
                cursor.execute("""
                    UPDATE consultants
                    SET qualifications = ?, bio = ?, years_of_experience = ?
                    WHERE id = ?
                """, (qualifications, bio, years_of_experience, consultant_id))
            else:
                cursor.execute("""
                    UPDATE consultants
                    SET qualifications = ?, bio = ?
                    WHERE id = ?
                """, (qualifications, bio, consultant_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def _row_to_entity(self, row) -> Consultant:
        keys = row.keys()
        return Consultant(
            id=row["id"],
            user_id=row["user_id"],
            bio=row["bio"],
            qualifications=row["qualifications"] if "qualifications" in keys else None,
            years_of_experience=row["years_of_experience"] if "years_of_experience" in keys else 0,
            is_active=bool(row["is_active"]) if "is_active" in keys else True,
            username=row["username"] if "username" in keys else None,
            email=row["email"] if "email" in keys else None,
            full_name=row["full_name"] if "full_name" in keys else None,
        )