from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.rating_repository import RatingRepository


class AbstractUnitOfWork(ABC):
    users: UserRepository
    books: BookRepository
    ratings: RatingRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...