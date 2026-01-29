# src/domain/repositories.py
from abc import ABC, abstractmethod
from typing import Optional, Iterable

from ..domains.entities.rating_entity import RatingEntity
    
class RatingRepository(ABC):
    @abstractmethod
    def get_for_user_and_book(self, user_id: int, book_id: int) -> Optional[RatingEntity]: ...
    
    @abstractmethod
    def add(self, rating: RatingEntity) -> RatingEntity: ...
    
    @abstractmethod
    def update(self, rating: RatingEntity) -> RatingEntity: ...

    @abstractmethod
    def get_for_user(self, user_id: int) -> Iterable[RatingEntity]: ...