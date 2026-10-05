"""Course repository — data access cho Course."""
from typing import Optional, List
from app.repositories.base_repository import BaseRepository
from app.models.course import Course


class CourseRepository(BaseRepository[Course]):

    def get_by_id(self, entity_id: int) -> Optional[Course]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            conn.close()

    def get_all(self) -> List[Course]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses ORDER BY created_at DESC")
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_published(self) -> List[Course]:
        """Chỉ lấy khóa học đã publish."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM courses WHERE is_published = 1 ORDER BY created_at DESC"
            )
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def search_by_title(self, keyword: str) -> List[Course]:
        """Tìm khóa học theo từ khóa trong title hoặc description."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM courses
                WHERE is_published = 1
                  AND (LOWER(title) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?))
                ORDER BY created_at DESC
            """, (f"%{keyword}%", f"%{keyword}%"))
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def create(self, course: Course) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO courses (title, description, category, level,
                                     is_published, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (course.title, course.description, course.category,
                  course.level, getattr(course, "is_published", True)))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update(self, course_id: int, data: dict) -> bool:
        """Cập nhật course với dict các field cần sửa."""
        if not data:
            return False
        allowed = {"title", "description", "category", "level", "is_published"}
        fields = [k for k in data.keys() if k in allowed]
        if not fields:
            return False

        set_clause = ", ".join(f"{f} = ?" for f in fields)
        values = [data[f] for f in fields] + [course_id]

        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE courses SET {set_clause} WHERE id = ?", values
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete(self, course_id: int) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def _row_to_entity(self, row) -> Course:
        keys = row.keys()
        return Course(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            category=row["category"] if "category" in keys else None,
            level=row["level"] if "level" in keys else None,
            is_published=bool(row["is_published"]) if "is_published" in keys else True,
            created_at=row["created_at"] if "created_at" in keys else None,
        )