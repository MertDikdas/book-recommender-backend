from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from src.database.database import SessionLocal
from src.services.recommendation_service import RecommendationService
from src.repositories.sqlalchemy_rating_repository import SqlAlchemyRatingRepository
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.repositories.sqlalchemy_book_repository import SqlAlchemyBookRepository


# Router for recommendations
router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# pydantic class for json body

class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str] 
    genre: Optional[str] 
    description: Optional[str]
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
@router.get("/{user_name}", response_model=List[BookOut])
def get_recommendations(
    user_name: str,
    page_number: int = 1,
    service: RecommendationService = Depends(get_recommendation_service)
):

    recommendations = service.get_recommendations_for_user(
        user_name, page_number
    )
    if recommendations is None:
        raise HTTPException(status_code=404, detail="User not found")
    return recommendations

@router.get("/{user_name}/{genre}", response_model=List[BookOut])
def get_recommendations_by_genre(
    user_name: str,
    genre: str,
    page_number: int = 1,
    service: RecommendationService = Depends(get_recommendation_service)
):

    recommendations = service.get_recommendations_for_user_by_genre(
        user_name,
        genre,
        page_number
    )
    if recommendations is None:
        raise HTTPException(status_code=404, detail="User not found")
    return recommendations