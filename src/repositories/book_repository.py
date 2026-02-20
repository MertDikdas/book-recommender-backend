from abc import ABC, abstractmethod
from typing import Optional, Iterable

from ..domains.entities import BookEntity, CommentEntity


class BookRepository(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[BookEntity]: ...

    @abstractmethod
    def add(self, book: BookEntity) -> BookEntity: ...

    @abstractmethod
    def list_all(self) -> list[BookEntity]: ...

    @abstractmethod
    def get_by_title(self, title: str) -> Optional[BookEntity]: ...

    @abstractmethod
    def search_books(self, query: str) -> list[BookEntity]: ...

    @abstractmethod
    def add_comment(self, book: BookEntity, query: str) -> BookEntity: ...

    @abstractmethod
    def get_comments_by_book_id(self, book_id:int) -> list[CommentEntity]: ...

    @abstractmethod
    def delete_comment_by_id(self,comment_id:int): ...