"""Enrollment repository — data access cho Enrollment."""
from typing import Optional, List
from app.repositories.base_repository import BaseRepository
from app.models.enrollment import Enrollment


class EnrollmentRepository(BaseRepository[Enrollment]):

    def get_by_id(self, entity_id: int) -> Optional[Enrollment]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, c.title AS course_title, c.category AS course_category,
                       c.level AS course_level
                FROM enrollments e
                JOIN courses c ON c.id = e.course_id
                WHERE e.id = ?
            """, (entity_id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            conn.close()

    def get_all(self) -> List[Enrollment]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, c.title AS course_title, c.category AS course_category,
                       c.level AS course_level
                FROM enrollments e
                JOIN courses c ON c.id = e.course_id
                ORDER BY e.enrolled_at DESC
            """)
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_by_user(self, user_id: int) -> List[Enrollment]:
        """Lấy tất cả enrollment của 1 user — dùng cho User Dashboard."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, c.title AS course_title, c.category AS course_category,
                       c.level AS course_level
                FROM enrollments e
                JOIN courses c ON c.id = e.course_id
                WHERE e.user_id = ?
                ORDER BY e.enrolled_at DESC
            """, (user_id,))
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Enrollment]:
        """Kiểm tra user đã enroll course chưa — chống duplicate."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, c.title AS course_title, c.category AS course_category,
                       c.level AS course_level
                FROM enrollments e
                JOIN courses c ON c.id = e.course_id
                WHERE e.user_id = ? AND e.course_id = ?
            """, (user_id, course_id))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            conn.close()

    def count_by_course(self, course_id: int) -> int:
        """Đếm số enrollment của 1 course — dùng cho report."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) AS cnt FROM enrollments WHERE course_id = ?",
                (course_id,)
            )
            return cursor.fetchone()["cnt"]
        finally:
            conn.close()

    def create(self, enrollment: Enrollment) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO enrollments (user_id, course_id, status, progress_percent)
                VALUES (?, ?, ?, ?)
            """, (enrollment.user_id, enrollment.course_id,
                  getattr(enrollment, "status", "ENROLLED"),
                  getattr(enrollment, "progress_percent", 0.0)))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_progress(self, enrollment_id: int, progress_percent: float,
                        status: str = "IN_PROGRESS") -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE enrollments
                SET progress_percent = ?,
                    status = ?,
                    completed_at = CASE WHEN ? >= 100.0
                                        THEN CURRENT_TIMESTAMP
                                        ELSE completed_at END
                WHERE id = ?
            """, (progress_percent, status, progress_percent, enrollment_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete(self, enrollment_id: int) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM enrollments WHERE id = ?", (enrollment_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def _row_to_entity(self, row) -> Enrollment:
        keys = row.keys()
        return Enrollment(
            id=row["id"],
            user_id=row["user_id"],
            course_id=row["course_id"],
            status=row["status"] if "status" in keys else "ENROLLED",
            progress_percent=row["progress_percent"] if "progress_percent" in keys else 0.0,
            enrolled_at=row["enrolled_at"] if "enrolled_at" in keys else None,
            completed_at=row["completed_at"] if "completed_at" in keys else None,
            course_title=row["course_title"] if "course_title" in keys else None,
            course_category=row["course_category"] if "course_category" in keys else None,
            course_level=row["course_level"] if "course_level" in keys else None,
        )