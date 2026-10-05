from typing import Optional, List
from .base_repository import BaseRepository
from app.models.lesson import Lesson


class LessonRepository(BaseRepository[Lesson]):
    """Data access repository for Lesson entities."""

    def get_by_id(self, entity_id: int) -> Optional[Lesson]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lessons WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Lesson(
                id=row["id"],
                course_id=row["course_id"],
                title=row["title"],
                content=row["content"] or "",
                video_url=row["video_url"],
                order_index=row["order_index"],
                duration_minutes=row["duration_minutes"] or 15
            )
        finally:
            conn.close()

    def get_by_course_id(self, course_id: int) -> List[Lesson]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lessons WHERE course_id = ? ORDER BY order_index ASC", (course_id,))
            rows = cursor.fetchall()
            return [
                Lesson(
                    id=r["id"],
                    course_id=r["course_id"],
                    title=r["title"],
                    content=r["content"] or "",
                    video_url=r["video_url"],
                    order_index=r["order_index"],
                    duration_minutes=r["duration_minutes"] or 15
                )
                for r in rows
            ]
        finally:
            conn.close()

    def get_all(self) -> List[Lesson]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lessons ORDER BY course_id ASC, order_index ASC")
            rows = cursor.fetchall()
            return [
                Lesson(
                    id=r["id"],
                    course_id=r["course_id"],
                    title=r["title"],
                    content=r["content"] or "",
                    video_url=r["video_url"],
                    order_index=r["order_index"],
                    duration_minutes=r["duration_minutes"] or 15
                )
                for r in rows
            ]
        finally:
            conn.close()

    def create(self, lesson: Lesson) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO lessons (course_id, title, content, video_url, order_index, duration_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    lesson.course_id,
                    lesson.title,
                    lesson.content,
                    lesson.video_url,
                    lesson.order_index,
                    lesson.duration_minutes
                )
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update(self, lesson: Lesson) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE lessons
                SET title = ?, content = ?, video_url = ?, order_index = ?, duration_minutes = ?
                WHERE id = ?
                """,
                (
                    lesson.title,
                    lesson.content,
                    lesson.video_url,
                    lesson.order_index,
                    lesson.duration_minutes,
                    lesson.id
                )
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

