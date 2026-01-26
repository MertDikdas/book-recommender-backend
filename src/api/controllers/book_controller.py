from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from src.database.database import SessionLocal
from src.services.book_service import BookService
from src.repositories.sqlalchemy_book_repository import SqlAlchemyBookRepository
from src.domains.orm.book_orm import BookORM
from src.mappers.entity_to_orm_mapper import user_entity_to_orm


router = APIRouter(prefix="/books", tags=["books"])

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None


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

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    repo = SqlAlchemyBookRepository(db)
    return BookService(repo)


@router.get("/all", response_model=List[BookOut])
def list_books(service: BookService = Depends(get_book_service)):
    books = service.list_books()
    return books

@router.get("/{book_name}", response_model=BookOut)
def get_book_by_name(book_name: str, 
                     service: BookService = Depends(get_book_service)):
    
    book = service.get_book_by_title(book_name)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("", response_model=BookOut)
def create_book(
    book_in: BookCreate,
    service: BookService = Depends(get_book_service),
):
    book = service.create_book(
        title=book_in.title,
        author=book_in.author,
        description=book_in.description,
        genre=book_in.genre,
    )
    return book