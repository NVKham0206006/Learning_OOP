from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class CommunityProgram:
    """Domain entity representing a community outreach or prevention program."""
    id: Optional[int]
    title: str
    description: str
    location: str
    start_date: date
    end_date: date
    max_participants: int = 100
    status: str = "upcoming"  # 'upcoming', 'ongoing', 'completed'
    created_at: Optional[datetime] = None


@dataclass
class ProgramParticipant:
    """Domain entity representing a user's participation in a community program."""
    id: Optional[int]
    program_id: int
    user_id: int
    status: str = "registered"  # 'registered', 'attended', 'cancelled'
    registered_at: Optional[datetime] = None

