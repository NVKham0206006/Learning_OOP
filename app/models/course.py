from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Course:
    """
    Domain entity representing an educational or prevention course.
    Includes encapsulation, basic validation, and relationship with Lessons.
    """
    id: Optional[int]
    title: str
    description: str
    category: str = "Phòng ngừa"
    level: str = "Cơ bản"  # 'Cơ bản', 'Trung cấp', 'Nâng cao'
    is_published: bool = True
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    lessons_count: int = 0

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.title or len(self.title.strip()) < 3:
            raise ValueError("Tiêu đề khóa học phải có ít nhất 3 ký tự.")
        valid_levels = ("Cơ bản", "Trung cấp", "Nâng cao", "Beginner", "Intermediate", "Advanced")
        if self.level not in valid_levels:
            raise ValueError(f"Cấp độ '{self.level}' không hợp lệ. Chọn một trong: {valid_levels}")

