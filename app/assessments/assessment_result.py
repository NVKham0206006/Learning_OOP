from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AssessmentResult:
    """The computed evaluation result of a user's completed assessment."""
    id: Optional[int]
    user_id: Optional[int]
    assessment_id: Optional[int]
    total_score: int
    risk_level: str  # 'LOW', 'MODERATE', 'HIGH'
    summary: str
    completed_at: Optional[datetime] = None

