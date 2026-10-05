from typing import Any
from .assessment_factory import AssessmentFactory
from app.assessments.assessment import Assessment
from app.assessments.craft_assessment import CraftAssessment


class CraftAssessmentFactory(AssessmentFactory):
    """
    Concrete Creator 2: Instantiates CraftAssessment (CRAFFT).
    """

    def create_assessment(self, **kwargs: Any) -> Assessment:
        return CraftAssessment(
            id=kwargs.get("id"),
            title=kwargs.get("title", "CRAFFT Adolescent Substance Screening"),
            description=kwargs.get(
                "description",
                "CRAFFT behavioral health screening tool designed specifically for youth & adolescents (12-21)."
            ),
            target_group=kwargs.get("target_group", "Adolescents (12-21)"),
            is_active=kwargs.get("is_active", True)
        )

