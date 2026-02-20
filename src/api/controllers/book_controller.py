from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from src.api.controllers.pydantic_models import BookCreate, CommentCreate, BookOut, CommentOut
from src.services.book_service import BookService
from src.uow.SqlAlchemyUOW import SqlAlchemyUnitOfWork


router = APIRouter(prefix="/books", tags=["books"])


# Dependency injection for BookService without UserRepository
def get_book_service() -> BookService:
    uow = SqlAlchemyUnitOfWork()
    return BookService(uow)


@router.get("/all", response_model=List[BookOut])
def list_all_books(service: BookService = Depends(get_book_service)):
    books = service.list_all_books()
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
    comment = service.create_comment(comment_in.book_id, comment_in.username, comment_in.comment_text)
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

@router.delete("/comments", status_code=204)
def delete_comment(
    comment_id: int,
    service: BookService = Depends(get_book_service)
):
    try:
        service.delete_comment_by_id(comment_id)
        return {"detail": "Comment deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))