"""Consultant service — profile, expertise, working schedule."""
from typing import Optional, List
from app.models.consultant import Consultant
from app.repositories.consultant_repository import ConsultantRepository
from app.repositories.working_schedule_repository import WorkingScheduleRepository


class ConsultantService:
    def __init__(self,
                 consultant_repo: ConsultantRepository = None,
                 schedule_repo: WorkingScheduleRepository = None):
        self.consultant_repo = consultant_repo or ConsultantRepository()
        self.schedule_repo = schedule_repo or WorkingScheduleRepository()

    def list_all(self) -> List[Consultant]:
        return self.consultant_repo.get_all()

    def search(self, keyword: str) -> List[Consultant]:
        if not keyword or not keyword.strip():
            return self.list_all()
        return self.consultant_repo.search_by_expertise(keyword.strip())

    def get_by_id(self, consultant_id: int) -> Optional[Consultant]:
        return self.consultant_repo.get_by_id(consultant_id)

    def get_by_user_id(self, user_id: int) -> Optional[Consultant]:
        return self.consultant_repo.get_by_user_id(user_id)

    def get_schedules(self, consultant_id: int) -> list:
        return self.schedule_repo.get_by_consultant(consultant_id)

    def update_profile(self, consultant_id: int, qualifications: str,
                       bio: str, years: int = None) -> bool:
        if not qualifications or not qualifications.strip():
            raise ValueError("Chuyên môn không được để trống.")
        return self.consultant_repo.update_expertise(
            consultant_id, qualifications.strip(), bio, years)