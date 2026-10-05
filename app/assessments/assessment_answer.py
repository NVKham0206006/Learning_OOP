from dataclasses import dataclass
from typing import Optional


@dataclass
class AssessmentAnswer:
    """Option answer choice for an assessment question."""
    id: Optional[int]
    question_id: int
    answer_text: str
    score_value: int = 0
    order_index: int = 1

