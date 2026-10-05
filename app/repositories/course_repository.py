from typing import Optional, List
from .base_repository import BaseRepository
from app.models.course import Course


class CourseRepository(BaseRepository[Course]):
    """Data access repository for Course entities."""

    def get_by_id(self, entity_id: int) -> Optional[Course]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT c.*, COUNT(l.id) AS lessons_count
                FROM courses c
                LEFT JOIN lessons l ON c.id = l.course_id
                WHERE c.id = ?
                GROUP BY c.id
                """,
                (entity_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return Course(
                id=row["id"],
                title=row["title"],
                description=row["description"] or "",
                category=row["category"] or "Phòng ngừa",
                level=row["level"] or "Cơ bản",
                is_published=bool(row["is_published"]),
                created_by=row["created_by"],
                lessons_count=row["lessons_count"]
            )
        finally:
            conn.close()

    def get_all(self, include_unpublished: bool = False) -> List[Course]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if include_unpublished:
                query = """
                SELECT c.*, COUNT(l.id) AS lessons_count
                FROM courses c
                LEFT JOIN lessons l ON c.id = l.course_id
                GROUP BY c.id
                ORDER BY c.id ASC
                """
                cursor.execute(query)
            else:
                query = """
                SELECT c.*, COUNT(l.id) AS lessons_count
                FROM courses c
                LEFT JOIN lessons l ON c.id = l.course_id
                WHERE c.is_published = 1
                GROUP BY c.id
                ORDER BY c.id ASC
                """
                cursor.execute(query)

            rows = cursor.fetchall()
            return [
                Course(
                    id=r["id"],
                    title=r["title"],
                    description=r["description"] or "",
                    category=r["category"] or "Phòng ngừa",
                    level=r["level"] or "Cơ bản",
                    is_published=bool(r["is_published"]),
                    created_by=r["created_by"],
                    lessons_count=r["lessons_count"]
                )
                for r in rows
            ]
        finally:
            conn.close()

    def create(self, course: Course) -> int:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO courses (title, description, category, level, is_published, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    course.title,
                    course.description,
                    course.category,
                    course.level,
                    int(course.is_published),
                    course.created_by
                )
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update(self, course: Course) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE courses
                SET title = ?, description = ?, category = ?, level = ?, is_published = ?
                WHERE id = ?
                """,
                (
                    course.title,
                    course.description,
                    course.category,
                    course.level,
                    int(course.is_published),
                    course.id
                )
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

