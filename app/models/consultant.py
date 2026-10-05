from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Consultant:
    """
    Domain entity representing a professional counselor or social worker.
    Includes encapsulation and domain validation.
    """
    id: Optional[int]
    user_id: int
    bio: str
    qualifications: str
    years_of_experience: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    # Joined field for convenient display
    full_name: Optional[str] = None
    email: Optional[str] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if self.years_of_experience < 0:
            raise ValueError("Số năm kinh nghiệm không thể là số âm.")
        if self.user_id <= 0:
            raise ValueError("user_id phải là số nguyên dương hợp lệ.")

