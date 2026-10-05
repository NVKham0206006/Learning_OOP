from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Lesson:
    """
    Domain entity representing an educational lesson within a course.
    Includes encapsulation and basic validation.
    """
    id: Optional[int]
    course_id: int
    title: str
    content: str
    video_url: Optional[str] = None
    order_index: int = 1
    duration_minutes: int = 15
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.title or len(self.title.strip()) < 3:
            raise ValueError("Tiêu đề bài học phải có ít nhất 3 ký tự.")
        if self.order_index < 1:
            raise ValueError("Thứ tự bài học phải >= 1.")
        if self.duration_minutes < 0:
            raise ValueError("Thời lượng bài học không thể âm.")

