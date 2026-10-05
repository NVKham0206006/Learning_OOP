from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from .assessment_question import AssessmentQuestion
from .assessment_result import AssessmentResult


@dataclass
class Assessment(ABC):
    """
    Abstract Product in Factory Method Pattern.
    Base domain class representing an assessment questionnaire.
    """
    id: Optional[int]
    title: str
    type: str  # 'ASSIST' or 'CRAFT'
    description: str
    target_group: str
    is_active: bool = True
    questions: List[AssessmentQuestion] = field(default_factory=list)
    created_at: Optional[datetime] = None

    @abstractmethod
    def calculate_risk(self, total_score: int) -> str:
        """Calculates risk level ('LOW', 'MODERATE', 'HIGH') based on total score."""
        pass

    @abstractmethod
    def get_evaluation_summary(self, total_score: int, risk_level: str) -> str:
        """Provides domain interpretation of the assessment score."""
        pass

    def evaluate(self, user_id: Optional[int], total_score: int) -> AssessmentResult:
        """Template evaluation method using polymorphic scoring methods."""
        risk_level = self.calculate_risk(total_score)
        summary = self.get_evaluation_summary(total_score, risk_level)
        return AssessmentResult(
            id=None,
            user_id=user_id,
            assessment_id=self.id,
            total_score=total_score,
            risk_level=risk_level,
            summary=summary,
            completed_at=datetime.now()
        )

