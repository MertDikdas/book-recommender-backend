from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.domains.entities import BookEntity, CommentEntity
from src.repositories.book_repository import BookRepository
from src.domains.orm import BookORM, CommentORM
from src.mappers.orm_to_entity_mapper import _book_orm_to_entity

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    # Getting book by id
    def get_by_id(self, book_id: int) -> Optional[BookEntity]:
        orm = self.db.query(BookORM).filter_by(id=book_id).first()
        return _book_orm_to_entity(orm) if orm else None
    
    # Adding a new book
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
    
    # Listing all books
    def list_all(self) -> list[BookEntity]:
        orms = self.db.query(BookORM).all()
        return [_book_orm_to_entity(orm) for orm in orms]
    
    # Getting book by title
    def get_by_title(self, title: str) -> Optional[BookEntity]:
        orm = self.db.query(BookORM).filter_by(title=title).first()
        return _book_orm_to_entity(orm) if orm else None
    
    # Searching books by title, author, or genre
    def search_books(self, query: str):
        pattern = f"%{query}%"

        books_orm = (
            self.db.query(BookORM)
            .filter(
                or_(
                    BookORM.title.ilike(pattern),
                    BookORM.author.ilike(pattern),
                    BookORM.genre.ilike(pattern),
                )
            )
            .order_by(BookORM.title)
            .limit(50)
            .all()
        )

        return [_book_orm_to_entity(orm) for orm in books_orm]

    def add_comment(self, book_id: int, user_id: int, comment_text: str) -> CommentEntity:
        comment = CommentORM(book_id=book_id, user_id=user_id, comment_text=comment_text)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return CommentEntity(
            id=comment.id,
            book_id=comment.book_id,
            user_id=comment.user_id,
            comment_text=comment.comment_text,
        )