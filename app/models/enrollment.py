from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Enrollment:
    """
    Domain entity representing a student's enrollment and progress in a course.
    Includes encapsulation, basic validation, and status transitions.
    """
    id: Optional[int]
    user_id: int
    course_id: int
    status: str = "enrolled"  # 'enrolled', 'in_progress', 'completed', 'dropped'
    progress_percent: float = 0.0
    enrolled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    # Joined course metadata for display
    course_title: Optional[str] = None
    course_category: Optional[str] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        valid_statuses = ("enrolled", "in_progress", "completed", "dropped")
        if self.status not in valid_statuses:
            raise ValueError(f"Trạng thái '{self.status}' không hợp lệ. Chọn một trong: {valid_statuses}")
        if not (0.0 <= self.progress_percent <= 100.0):
            raise ValueError("Tiến độ khóa học phải trong khoảng từ 0% đến 100%.")

    def update_progress(self, percent: float) -> None:
        """Encapsulated business logic to update enrollment progress."""
        self.progress_percent = min(100.0, max(0.0, percent))
        if self.progress_percent >= 100.0:
            self.status = "completed"
            self.completed_at = datetime.now()
        elif self.progress_percent > 0.0:
            self.status = "in_progress"
        self.validate()

