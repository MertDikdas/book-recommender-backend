from abc import ABC, abstractmethod
from typing import Optional, Iterable

from ..domains.entities.book_entity import BookEntity


class BookRepository(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[BookEntity]: ...