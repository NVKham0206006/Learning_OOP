from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from app.database.connection import get_db_connection

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Abstract generic repository defining standard persistence contracts.
    Decouples domain models and services from specific database implementations.
    """

    def __init__(self, db_connection_factory=None):
        self.get_connection = db_connection_factory or get_db_connection

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

