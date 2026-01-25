from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict

from scripts.database import SessionLocal
from src.services.user_service import UserService
from scripts.sqlalchemy_repositories.user_repository import SqlAlchemyUserRepository


router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    username: str


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = SqlAlchemyUserRepository(db)   # ✅ DOĞRU OLAN BU
    return UserService(repo)


@router.post("", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.create_user(user_in.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten mevcut")
    return user
