from abc import ABC, abstractmethod
from typing import Optional, Iterable

from ..domains.models import Book


class BookRepository(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]: ...