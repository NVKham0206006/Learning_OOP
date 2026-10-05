from typing import Any
from .assessment_factory import AssessmentFactory
from app.assessments.assessment import Assessment
from app.assessments.assist_assessment import AssistAssessment


class AssistAssessmentFactory(AssessmentFactory):
    """
    Concrete Creator 1: Instantiates AssistAssessment (WHO ASSIST).
    """

    def create_assessment(self, **kwargs: Any) -> Assessment:
        return AssistAssessment(
            id=kwargs.get("id"),
            title=kwargs.get("title", "WHO ASSIST Substance Screening"),
            description=kwargs.get(
                "description",
                "WHO Alcohol, Smoking and Substance Involvement Screening Test for adults (18+)."
            ),
            target_group=kwargs.get("target_group", "Adults (18+)"),
            is_active=kwargs.get("is_active", True)
        )

