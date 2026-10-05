"""Course service — CRUD, enrollment, progress."""
from typing import Optional, List
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.enrollment import Enrollment
from app.repositories.course_repository import CourseRepository
from app.repositories.lesson_repository import LessonRepository
from app.repositories.enrollment_repository import EnrollmentRepository


class CourseService:
    def __init__(self,
                 course_repo: CourseRepository = None,
                 lesson_repo: LessonRepository = None,
                 enrollment_repo: EnrollmentRepository = None):
        self.course_repo = course_repo or CourseRepository()
        self.lesson_repo = lesson_repo or LessonRepository()
        self.enrollment_repo = enrollment_repo or EnrollmentRepository()

    # ==================== PUBLIC ====================
    def list_published(self) -> List[Course]:
        return self.course_repo.get_published()

    def search(self, keyword: str) -> List[Course]:
        if not keyword or not keyword.strip():
            return self.list_published()
        return self.course_repo.search_by_title(keyword.strip())

    def get_by_id(self, course_id: int) -> Optional[Course]:
        return self.course_repo.get_by_id(course_id)

    def get_lessons(self, course_id: int) -> List[Lesson]:
        return self.lesson_repo.get_by_course(course_id)

    # ==================== USER ====================
    def enroll(self, user_id: int, course_id: int) -> Enrollment:
        """Đăng ký khóa học — chống duplicate."""
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise ValueError("Khóa học không tồn tại.")

        existing = self.enrollment_repo.get_by_user_and_course(user_id, course_id)
        if existing:
            if existing.status == "dropped":
                # Cho phép re-enroll
                self.enrollment_repo.update_progress(existing.id, 0.0, "enrolled")
                return existing
            raise ValueError("Bạn đã đăng ký khóa học này rồi.")

        enrollment = Enrollment(
            id=None,
            user_id=user_id,
            course_id=course_id,
            status="enrolled",
            progress_percent=0.0,
        )
        enrollment_id = self.enrollment_repo.create(enrollment)
        enrollment.id = enrollment_id
        return enrollment

    def get_user_enrollments(self, user_id: int) -> List[Enrollment]:
        return self.enrollment_repo.get_by_user(user_id)

    def update_progress(self, enrollment_id: int, percent: float) -> bool:
        if not (0.0 <= percent <= 100.0):
            raise ValueError("Tiến độ phải trong khoảng 0–100%.")
        status = "completed" if percent >= 100.0 else ("in_progress" if percent > 0 else "enrolled")
        return self.enrollment_repo.update_progress(enrollment_id, percent, status)

    # ==================== ADMIN ====================
    def admin_list_all(self) -> List[Course]:
        return self.course_repo.get_all()

    def admin_create(self, title: str, description: str,
                     category: str = "Phòng ngừa", level: str = "Cơ bản") -> Course:
        if not title or not title.strip():
            raise ValueError("Tiêu đề khóa học không được để trống.")
        course = Course(
            id=None,
            title=title.strip(),
            description=description,
            category=category,
            level=level,
            is_published=True,
        )
        course_id = self.course_repo.create(course)
        course.id = course_id
        return course

    def admin_update(self, course_id: int, data: dict) -> bool:
        if not self.course_repo.get_by_id(course_id):
            raise ValueError("Khóa học không tồn tại.")
        return self.course_repo.update(course_id, data)

    def admin_delete(self, course_id: int) -> bool:
        return self.course_repo.delete(course_id)