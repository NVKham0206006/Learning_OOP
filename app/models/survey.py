from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Survey:
    """Domain entity representing a community feedback survey."""
    id: Optional[int]
    title: str
    description: str
    is_active: bool = True
    created_at: Optional[datetime] = None


@dataclass
class SurveyResponse:
    """Domain entity representing an individual response to a survey."""
    id: Optional[int]
    survey_id: int
    user_id: Optional[int]
    response_data: str  # JSON payload
    submitted_at: Optional[datetime] = None

