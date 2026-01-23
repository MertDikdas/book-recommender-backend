# src/domain/repositories.py
from abc import ABC, abstractmethod
from typing import Optional, Iterable

from ..domains.models import User, Book, Rating
    
class RatingRepository(ABC):
    @abstractmethod
    def get_for_user_and_book(self, user_id: int, book_id: int) -> Optional[Rating]: ...
    
    @abstractmethod
    def add(self, rating: Rating) -> Rating: ...
    
    @abstractmethod
    def update(self, rating: Rating) -> Rating: ...
