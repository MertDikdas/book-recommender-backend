from fastapi import APIRouter, Depends, HTTPException

from typing import List
from src.api.controllers.pydantic_models import BookOut
from src.services.recommendation_service import RecommendationService
from src.uow.SqlAlchemyUOW import SqlAlchemyUnitOfWork
# Router for recommendations
router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_service() -> RecommendationService:
    uow = SqlAlchemyUnitOfWork()
    return RecommendationService(uow)

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