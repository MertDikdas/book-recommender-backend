from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.database.database import SessionLocal
from src.services.user_service import UserService
from src.services.book_service import BookService
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.repositories.sqlalchemy_book_repository import SqlAlchemyBookRepository
from src.repositories.sqlalchemy_rating_repository import SqlAlchemyRatingRepository
from src.mappers.entity_to_orm_mapper import user_entity_to_orm

#Router for user
router = APIRouter(prefix="/users", tags=["users"])

#pydantic class for json body
class UserCreate(BaseModel):
    username: str


class UserOut(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str]
    genre: Optional[str]

    model_config = ConfigDict(from_attributes=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#for accessing service with db
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    book_repo = SqlAlchemyBookRepository(db)
    user_repo = SqlAlchemyUserRepository(db)  # Assuming you have a function to create a UserRepository
    rating_repo = SqlAlchemyRatingRepository(db)  # Assuming you have a function to create a RatingRepository
    return UserService(book_repo=book_repo, user_repo=user_repo, rating_repo=rating_repo)

#creates user
@router.post("", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.create_user(user_in.username)
    if user is None:
        raise HTTPException(status_code=400, detail="User already exists!")
    return user

#get user
@router.get("", response_model=UserOut)
def get_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user(user_in.username)
    if user is None:
        raise HTTPException(status_code=400, detail = "User doesn't exists!")
    orm = user_entity_to_orm(user);
    return orm

@router.get("/{username}/books", response_model=List[BookOut])
def get_user_books(
    username: str,
    service: UserService = Depends(get_user_service),
):
    books = service.get_user_books(username)

    if not books:
        raise HTTPException(status_code=404, detail="User has no books")
    return books