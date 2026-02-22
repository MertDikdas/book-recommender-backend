# scripts/repositories.py
from typing import Optional
from sqlalchemy.orm import Session
from src.domains.entities.rating_entity import RatingEntity
from src.repositories.rating_repository import RatingRepository
from src.domains.orm.rating_orm import RatingORM
from src.mappers.orm_to_entity_mapper import _rating_orm_to_entity


class SqlAlchemyRatingRepository(RatingRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_for_user_and_book(self, user_id: int, book_id: int) -> Optional[RatingEntity]:
        orm = (
            self.db.query(RatingORM)
            .filter_by(user_id=user_id, book_id=book_id)
            .first()
        )
        return _rating_orm_to_entity(orm) if orm else None

    def add(self, rating: RatingEntity) -> RatingEntity:
        orm = RatingORM(
            user_id=rating.user_id,
            book_id=rating.book_id,
            rating=rating.rating,
        )
        self.db.add(orm)
        self.db.flush()
        self.db.refresh(orm)
        return _rating_orm_to_entity(orm)

    def update(self, rating: RatingEntity) -> RatingEntity:
        orm = (
            self.db.query(RatingORM)
            .filter_by(id=rating.id)
            .first()
        )
        if orm is None:
            raise ValueError("Rating not found")

        orm.rating = rating.rating
        self.db.flush()
        self.db.refresh(orm)
        return _rating_orm_to_entity(orm)
    
    def get_for_user(self, user_id: int) -> list[RatingEntity]:
        orms = self.db.query(RatingORM).filter_by(user_id=user_id).all()
        return [_rating_orm_to_entity(orm) for orm in orms]
    
    def delete(self, rating_id):
        orm = self.db.query(RatingORM).filter_by(id=rating_id).first()
        if orm:
            self.db.delete(orm)