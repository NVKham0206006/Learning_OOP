from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Recommendation:
    """Domain entity representing guidance recommended after an assessment."""
    id: Optional[int]
    assessment_result_id: int
    title: str
    advice_text: str
    recommended_action: Optional[str] = None
    suggested_course_id: Optional[int] = None
    created_at: Optional[datetime] = None

