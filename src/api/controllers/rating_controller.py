from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.api.controllers.pydantic_models import RatingCreate, RatingOut
from src.services.rating_service import RatingService
from src.uow.SqlAlchemyUOW import SqlAlchemyUnitOfWork
router = APIRouter(prefix="/ratings", tags=["ratings"])


def get_rating_service() -> RatingService:
    uow = SqlAlchemyUnitOfWork()
    return RatingService(uow)

#Create rating
@router.post("", response_model=RatingOut)
def create_rating(
    rating_in: RatingCreate,
    service: RatingService = Depends(get_rating_service),
):
    rating = service.rate_book(
        rating_in.username,
        rating_in.book_id,
        rating_in.rating,
    )
    if rating is None:
        raise HTTPException(status_code=400, detail="Could not create or update rating")
    return rating

#Get rating for user and book
@router.get("/user/{username}/book/{book_id}", response_model=RatingOut)
def get_rating_for_user_and_book(
    username: str,
    book_id: int,
    service: RatingService = Depends(get_rating_service),
):
    rating = service.get_rating_for_user_and_book(username, book_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

#Get ratings for user
@router.get("/user/{username}", response_model=List[RatingOut])
def get_ratings_for_user(
    username: str,
    service: RatingService = Depends(get_rating_service),
):
    ratings = service.get_ratings_for_user(username)
    return ratings

@router.delete("/{username}/books/{book_id}")
def delete_user_book(
    username: str,
    book_id: int,
    service: RatingService = Depends(get_rating_service),
):
    deleted = service.delete_user_book(username, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found or not owned by user")