from abc import ABC, abstractmethod
from typing import Any
from app.assessments.assessment import Assessment


class AssessmentFactory(ABC):
    """
    Abstract Creator in Factory Method Pattern.
    Declares the factory method createAssessment() that returns an Assessment object.
    """

    @abstractmethod
    def create_assessment(self, **kwargs: Any) -> Assessment:
        """
        Factory Method: Creates and returns a concrete Assessment instance.
        """
        pass

    def createAssessment(self, **kwargs: Any) -> Assessment:
        """CamelCase alias matching specification."""
        return self.create_assessment(**kwargs)

    def prepare_assessment(self, **kwargs: Any) -> Assessment:
        """Template Creator operation."""
        assessment = self.create_assessment(**kwargs)
        return assessment

