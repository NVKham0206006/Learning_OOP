from dataclasses import dataclass
from typing import Optional
from .assessment import Assessment


@dataclass
class AssistAssessment(Assessment):
    """
    Concrete Product 1: ASSIST (Alcohol, Smoking and Substance Involvement Screening Test).
    Standard screening questionnaire developed by WHO for adults (18+).
    """

    def __init__(
        self,
        id: Optional[int] = None,
        title: str = "WHO ASSIST Substance Screening",
        description: str = "WHO Alcohol, Smoking and Substance Involvement Screening Test for adults (18+).",
        target_group: str = "Adults (18+)",
        is_active: bool = True
    ):
        super().__init__(
            id=id,
            title=title,
            type="ASSIST",
            description=description,
            target_group=target_group,
            is_active=is_active
        )

    def calculate_risk(self, total_score: int) -> str:
        """
        WHO ASSIST scoring standards:
        - 0-3: Low risk
        - 4-26: Moderate risk
        - 27+: High risk
        """
        if total_score <= 3:
            return "LOW"
        elif total_score <= 26:
            return "MODERATE"
        else:
            return "HIGH"

    def get_evaluation_summary(self, total_score: int, risk_level: str) -> str:
        if risk_level == "LOW":
            return (
                f"Điểm số ASSIST của bạn là {total_score}. Mức độ rủi ro THẤP (LOW). "
                "Bạn có nguy cơ thấp về các vấn đề liên quan đến sử dụng chất. Khuyến nghị duy trì lối sống lành mạnh."
            )
        elif risk_level == "MODERATE":
            return (
                f"Điểm số ASSIST của bạn là {total_score}. Mức độ rủi ro TRUNG BÌNH (MODERATE). "
                "Bạn có nguy cơ gặp phải các vấn đề sức khỏe hoặc xã hội. Khuyến nghị can thiệp ngắn và tham gia khóa học phòng ngừa."
            )
        else:
            return (
                f"Điểm số ASSIST của bạn là {total_score}. Mức độ rủi ro CAO (HIGH). "
                "Bạn có nguy cơ cao phụ thuộc chất và các tác hại nghiêm trọng. Khuyến nghị đặt lịch tư vấn chuyên gia ngay lập tức."
            )

