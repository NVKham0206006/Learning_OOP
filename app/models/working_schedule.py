from dataclasses import dataclass
from typing import Optional


@dataclass
class WorkingSchedule:
    """
    Domain entity representing a consultant's available working slot.
    Includes encapsulation, validation, and localized day name.
    """
    id: Optional[int]
    consultant_id: int
    day_of_week: int  # 0 = Thứ 2, ..., 6 = Chủ nhật
    start_time: str   # HH:MM
    end_time: str     # HH:MM
    is_available: bool = True

    DAY_NAMES = [
        "Thứ Hai",
        "Thứ Ba",
        "Thứ Tư",
        "Thứ Năm",
        "Thứ Sáu",
        "Thứ Bảy",
        "Chủ Nhật",
    ]

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not (0 <= self.day_of_week <= 6):
            raise ValueError("day_of_week phải nằm trong khoảng từ 0 (Thứ Hai) đến 6 (Chủ Nhật).")
        if not self.start_time or not self.end_time:
            raise ValueError("Giờ bắt đầu và giờ kết thúc không được để trống.")
        if self.start_time >= self.end_time:
            raise ValueError("Giờ bắt đầu phải trước giờ kết thúc.")

    @property
    def day_name(self) -> str:
        return self.DAY_NAMES[self.day_of_week]

