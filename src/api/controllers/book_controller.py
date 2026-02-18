from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from src.database.database import SessionLocal
from src.services.book_service import BookService
from src.repositories.sqlalchemy_book_repository import SqlAlchemyBookRepository
from src.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from src.repositories.sqlalchemy_rating_repository import SqlAlchemyRatingRepository
from src.domains.orm.book_orm import BookORM
from src.mappers.entity_to_orm_mapper import user_entity_to_orm


router = APIRouter(prefix="/books", tags=["books"])

class BookCreate(BaseModel):
    title: str
    work_key: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    img_cover_url : Optional[str] = None

class CommentCreate(BaseModel):
    book_id:int
    user_id: int
    comment_text:str = Field(min_length=1, max_length=2000)

class BookOut(BaseModel):
    id: int
    work_key: str
    title: str
    author: str
    genre: Optional[str] = None
    description: Optional[str] = None
    img_cover_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CommentOut(BaseModel):
    book_id: int
    user_id: int
    comment_text:str
    
    model_config = ConfigDict(from_attributes=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency injection for BookService without UserRepository
def get_book_service(db: Session = Depends(get_db)) -> BookService:
    book_repo = SqlAlchemyBookRepository(db)
    user_repo = SqlAlchemyUserRepository(db)
    return BookService(book_repo=book_repo, user_repo=user_repo)


@router.get("/all", response_model=List[BookOut])
def list_books(service: BookService = Depends(get_book_service)):
    books = service.list_books()
    return books

@router.get("/by-title/{book_name}", response_model=BookOut)
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

@router.get("/search", response_model=List[BookOut])
def search_books(
    q: str = Query(...),
    service: BookService = Depends(get_book_service),
):
    if not q.strip():
        return []
    books = service.search_books(q)
    return books

@router.post("/comments", response_model=CommentOut)
def create_comment(
    comment_in: CommentCreate,               
    service: BookService = Depends(get_book_service)
):
    comment = service.create_comment(comment_in.book_id, comment_in.user_id, comment_in.comment_text)
    return comment

@router.get("/comments", response_model=list[CommentOut])
def get_comments(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    comments = service.get_comments_by_book_id(book_id)
    if comments is None:
        return []
    return comments
