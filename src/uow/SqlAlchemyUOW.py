# src/uow/sqlalchemy_uow.py
from typing import Callable
from sqlalchemy.orm import Session

from src.database.database import SessionLocal
from src.uow.AbstractUOW import AbstractUnitOfWork
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.repositories.sqlalchemy_book_repository import SqlAlchemyBookRepository
from src.repositories.sqlalchemy_rating_repository import SqlAlchemyRatingRepository


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Callable[[], Session] = SessionLocal):
        self.session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self.session_factory()

        # Repositories aynı session'ı paylaşacak
        self.users = SqlAlchemyUserRepository(self.session)
        self.books = SqlAlchemyBookRepository(self.session)
        self.ratings = SqlAlchemyRatingRepository(self.session)

        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.rollback()
        else:
            # commit'i servisten manuel de çağırabilirsin, istersen buraya koyma
            pass
        if self.session:
            self.session.close()

    def commit(self) -> None:
        if self.session:
            print("Succesfull")
            self.session.commit()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()