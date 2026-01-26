from typing import Optional
from sqlalchemy.orm import Session
from src.domains.entities.book_entity import BookEntity
from src.repositories.book_repository import BookRepository
from src.domains.orm.book_orm import BookORM
from src.mappers.orm_to_entity_mapper import _book_orm_to_entity

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, book_id: int) -> Optional[BookEntity]:
        orm = self.db.query(BookORM).filter_by(id=book_id).first()
        return _book_orm_to_entity(orm) if orm else None
    
    def add(self, book: BookEntity) -> BookEntity:
        orm = BookORM(
            title=book.title,
            author=book.author,
            description=book.description,
            genre=book.genre,
        )
        self.db.add(orm)
        self.db.flush()   # id oluşsun
        self.db.refresh(orm)
        self.db.commit()
        return _book_orm_to_entity(orm)
    
    def list_all(self) -> list[BookEntity]:
        orms = self.db.query(BookORM).all()
        return [_book_orm_to_entity(orm) for orm in orms]
    
    def get_by_title(self, title: str) -> Optional[BookEntity]:
        orm = self.db.query(BookORM).filter_by(title=title).first()
        return _book_orm_to_entity(orm) if orm else None