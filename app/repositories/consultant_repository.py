from typing import Optional, List
from .base_repository import BaseRepository
from app.models.consultant import Consultant


class ConsultantRepository(BaseRepository[Consultant]):
    """Data access repository for Consultant entities."""

    def get_by_id(self, entity_id: int) -> Optional[Consultant]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT c.*, u.full_name, u.email
                FROM consultants c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = ?
                """,
                (entity_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return Consultant(
                id=row["id"],
                user_id=row["user_id"],
                bio=row["bio"] or "",
                qualifications=row["qualifications"] or "",
                years_of_experience=row["years_of_experience"] or 0,
                is_active=bool(row["is_active"]),
                full_name=row["full_name"],
                email=row["email"]
            )
        finally:
            conn.close()

    def get_by_user_id(self, user_id: int) -> Optional[Consultant]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT c.*, u.full_name, u.email
                FROM consultants c
                JOIN users u ON c.user_id = u.id
                WHERE c.user_id = ?
                """,
                (user_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return Consultant(
                id=row["id"],
                user_id=row["user_id"],
                bio=row["bio"] or "",
                qualifications=row["qualifications"] or "",
                years_of_experience=row["years_of_experience"] or 0,
                is_active=bool(row["is_active"]),
                full_name=row["full_name"],
                email=row["email"]
            )
        finally:
            conn.close()

    def get_all(self) -> List[Consultant]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT c.*, u.full_name, u.email
                FROM consultants c
                JOIN users u ON c.user_id = u.id
                ORDER BY c.id ASC
                """
            )
            rows = cursor.fetchall()
            return [
                Consultant(
                    id=r["id"],
                    user_id=r["user_id"],
                    bio=r["bio"] or "",
                    qualifications=r["qualifications"] or "",
                    years_of_experience=r["years_of_experience"] or 0,
                    is_active=bool(r["is_active"]),
                    full_name=r["full_name"],
                    email=r["email"]
                )
                for r in rows
            ]
        finally:
            conn.close()

    def create(self, consultant: Consultant) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO consultants (user_id, bio, qualifications, years_of_experience, is_active)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    consultant.user_id,
                    consultant.bio,
                    consultant.qualifications,
                    consultant.years_of_experience,
                    int(consultant.is_active)
                )
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_expertise(self, user_id: int, bio: str, qualifications: str, years_of_experience: int) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE consultants
                SET bio = ?, qualifications = ?, years_of_experience = ?
                WHERE user_id = ?
                """,
                (bio, qualifications, years_of_experience, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

