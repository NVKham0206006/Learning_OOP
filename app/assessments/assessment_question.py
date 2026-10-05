from dataclasses import dataclass, field
from typing import Optional, List
from .assessment_answer import AssessmentAnswer


@dataclass
class AssessmentQuestion:
    """A question within an assessment questionnaire."""
    id: Optional[int]
    assessment_id: int
    question_code: str
    question_text: str
    order_index: int = 1
    weight: float = 1.0
    options: List[AssessmentAnswer] = field(default_factory=list)

