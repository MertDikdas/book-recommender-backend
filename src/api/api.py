from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy.orm import Session

from src.database.database import Base, SessionLocal, engine
from src.domains.orm import User, Book, Rating
from src.api.controllers.user_controller import router as user_router



app = FastAPI(title="Book Recommender API")

app.include_router(user_router)

# ---------- DB dependency ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Pydantic şemaları ----------

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None


class RatingCreate(BaseModel):
    username: str
    book_id: int
    rating: int


class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str]
    genre: Optional[str]

    class Config:
        orm_mode = True


class RatingOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int

    class Config:
        orm_mode = True


# ---------- Helper: user getir / oluştur ----------

def get_or_create_user(db: Session, username: str) -> User:
    user = db.query(User).filter_by(username=username).first()
    if user:
        return user

    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- CONTROLLER / ENDPOINTLER ----------

@app.post("/books", response_model=BookOut, tags=["books"])
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    book = Book(
        title=book_in.title,
        author=book_in.author,
        genre=book_in.genre,
        description=book_in.description,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books", response_model=List[BookOut], tags=["books"])
def list_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@app.post("/ratings", response_model=RatingOut, tags=["ratings"])
def create_or_update_rating(rating_in: RatingCreate, db: Session = Depends(get_db)):
    # rating 1–5 arası kontrol
    if not (1 <= rating_in.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating 1 ile 5 arasında olmalı")

    # user getir / oluştur
    user = get_or_create_user(db, rating_in.username)

    # kitap var mı?
    book = db.query(Book).filter_by(id=rating_in.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # aynı user+book için rating varsa update et
    existing = (
        db.query(Rating)
        .filter_by(user_id=user.id, book_id=book.id)
        .first()
    )
    if existing:
        existing.rating = rating_in.rating
        db.commit()
        db.refresh(existing)
        return existing

    # yoksa yeni rating
    rating = Rating(
        user_id=user.id,
        book_id=book.id,
        rating=rating_in.rating,
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


@app.get("/users/{username}/ratings", response_model=List[RatingOut], tags=["ratings"])
def get_user_ratings(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ratings = db.query(Rating).filter_by(user_id=user.id).all()
    return ratings
