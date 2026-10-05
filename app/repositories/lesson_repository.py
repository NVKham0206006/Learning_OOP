"""Lesson repository — data access cho Lesson."""
from typing import Optional, List
from app.repositories.base_repository import BaseRepository
from app.models.lesson import Lesson


class LessonRepository(BaseRepository[Lesson]):

    def get_by_id(self, entity_id: int) -> Optional[Lesson]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lessons WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            conn.close()

    def get_all(self) -> List[Lesson]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM lessons ORDER BY course_id, order_index ASC"
            )
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def get_by_course(self, course_id: int) -> List[Lesson]:
        """Lấy lessons của 1 course, sắp theo order_index."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM lessons
                WHERE course_id = ?
                ORDER BY order_index ASC
            """, (course_id,))
            return [self._row_to_entity(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    def create(self, lesson: Lesson) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO lessons (course_id, title, content, order_index, duration_minutes)
                VALUES (?, ?, ?, ?, ?)
            """, (lesson.course_id, lesson.title, lesson.content,
                  lesson.order_index, getattr(lesson, "duration_minutes", 0)))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update(self, lesson_id: int, data: dict) -> bool:
        if not data:
            return False
        allowed = {"title", "content", "order_index", "duration_minutes"}
        fields = [k for k in data.keys() if k in allowed]
        if not fields:
            return False

        set_clause = ", ".join(f"{f} = ?" for f in fields)
        values = [data[f] for f in fields] + [lesson_id]

        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE lessons SET {set_clause} WHERE id = ?", values
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete(self, lesson_id: int) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def _row_to_entity(self, row) -> Lesson:
        keys = row.keys()
        return Lesson(
            id=row["id"],
            course_id=row["course_id"],
            title=row["title"],
            content=row["content"],
            order_index=row["order_index"],
            duration_minutes=row["duration_minutes"] if "duration_minutes" in keys else 0,
        )