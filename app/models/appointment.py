from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Appointment:
    """Domain entity representing a counseling appointment."""
    id: Optional[int]
    user_id: int
    consultant_id: int
    scheduled_time: datetime
    status: str = "pending"  # 'pending', 'confirmed', 'completed', 'cancelled'
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    def confirm(self) -> None:
        self.status = "confirmed"

    def cancel(self, reason: Optional[str] = None) -> None:
        self.status = "cancelled"
        if reason:
            self.notes = f"{self.notes or ''} [Đã hủy: {reason}]"

    def complete(self) -> None:
        self.status = "completed"

