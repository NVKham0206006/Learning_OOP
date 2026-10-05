from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BlogPost:
    """Domain entity representing an educational or awareness article."""
    id: Optional[int]
    author_id: int
    title: str
    slug: str
    summary: str
    content: str
    is_published: bool = True
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

