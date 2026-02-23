from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.services.user_service import UserService
from src.api.controllers.pydantic_models import UserCreate, UserOut, BookOut
from src.uow.SqlAlchemyUOW import SqlAlchemyUnitOfWork
#Router for user
router = APIRouter(prefix="/users", tags=["users"])

#for accessing service with db
def get_user_service() -> UserService:
    uow = SqlAlchemyUnitOfWork()
    return UserService(uow)


@router.get("/by-id", response_model=UserOut)
def get_user_books(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

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
@router.get("/{username}", response_model=UserOut)
def get_user(
    username: str,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user(username)
    if user is None:
        raise HTTPException(status_code=400, detail = "User doesn't exists!")
    return user

@router.get("/{username}/books", response_model=List[BookOut])
def get_user_books(
    username: str,
    service: UserService = Depends(get_user_service),
):
    books = list(service.get_user_books(username))

    if not books:
        raise HTTPException(status_code=404, detail="User has no books")
    return books

@router.delete("/{username}", status_code=204)
def delete_user(
    username: str,
    service: UserService = Depends(get_user_service),
):
    try:
        service.delete_user(username)
        return {"detail": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{username}/genres", response_model=List[str])
def get_user_genres(
    username: str,
    service: UserService = Depends(get_user_service),
):
    genres = service.get_user_genres(username)
    if not genres:
        raise HTTPException(status_code=404, detail="User has no genres")
    return genres

