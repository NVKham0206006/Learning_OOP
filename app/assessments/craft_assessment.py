from dataclasses import dataclass
from typing import Optional
from .assessment import Assessment


@dataclass
class CraftAssessment(Assessment):
    """
    Concrete Product 2: CRAFFT Adolescent Substance Screening Tool (12-21).
    """

    def __init__(
        self,
        id: Optional[int] = None,
        title: str = "CRAFFT Adolescent Substance Screening",
        description: str = "CRAFFT behavioral health screening tool designed specifically for youth & adolescents (12-21).",
        target_group: str = "Adolescents (12-21)",
        is_active: bool = True
    ):
        super().__init__(
            id=id,
            title=title,
            type="CRAFT",
            description=description,
            target_group=target_group,
            is_active=is_active
        )

    def calculate_risk(self, total_score: int) -> str:
        if total_score <= 0:
            return "LOW"
        elif total_score == 1:
            return "MODERATE"
        else:
            return "HIGH"

    def get_evaluation_summary(self, total_score: int, risk_level: str) -> str:
        if risk_level == "LOW":
            return (
                f"Điểm số CRAFFT của bạn là {total_score}/6. Mức độ rủi ro THẤP (LOW). "
                "Không có dấu hiệu rủi ro nghiêm trọng về hành vi sử dụng chất ở thanh thiếu niên."
            )
        elif risk_level == "MODERATE":
            return (
                f"Điểm số CRAFFT của bạn là {total_score}/6. Mức độ rủi ro TRUNG BÌNH (MODERATE). "
                "Có một số dấu hiệu cảnh báo ban đầu về sử dụng chất. Khuyến nghị tham gia khóa học kỹ năng từ chối."
            )
        else:
            return (
                f"Điểm số CRAFFT của bạn là {total_score}/6. Mức độ rủi ro CAO (HIGH). "
                "Điểm số từ 2 trở lên cho thấy nguy cơ cao có rối loạn sử dụng chất. Khuyến nghị gặp chuyên gia tư vấn."
            )

