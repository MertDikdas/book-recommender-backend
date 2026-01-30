from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict
from src.database.database import SessionLocal
from src.services.recommendation_service import RecommendationService
from src.repositories.sqlalchemy_rating_repository import SqlAlchemyRatingRepository
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.repositories.sqlalchemy_book_repository import SqlAlchemyBookRepository

# Router for recommendations
router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# pydantic class for json body

class RecommendationRequest(BaseModel):
    user_id: int
    top_k: int = 10

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    description: str
    model_config = ConfigDict(from_attributes=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_recommendation_service(
    db: Session = Depends(get_db),
) -> RecommendationService:
    user_repo = SqlAlchemyUserRepository(db)
    book_repo = SqlAlchemyBookRepository(db)
    rating_repo = SqlAlchemyRatingRepository(db)
    return RecommendationService(user_repo, book_repo, rating_repo)

# for accessing service with db
@router.get("", response_model=List[BookOut])
def get_recommendations(
    user_id: int,
    service: RecommendationService = Depends(get_recommendation_service)
):

    recommendations = service.get_recommendations_for_user(
        user_id,
    )
    return recommendations