from typing import Optional
from sqlalchemy.orm import Session
from domains.entities.models import Book as BookEntity
from src.repositories.book_repository import BookRepository
from src.domains.orm import Book as BookORM
from scripts.mapper.orm_to_entity_mapper import _book_orm_to_entity

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, book_id: int) -> Optional[BookEntity]:
        orm = self.db.query(BookORM).filter_by(id=book_id).first()
        return _book_orm_to_entity(orm) if orm else None