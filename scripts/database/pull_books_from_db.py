from sqlalchemy.orm import Session
from scripts.models import Book, Rating, User
import pandas as pd

def pull_books_from_db(db: Session) -> pd.DataFrame:
    books = db.query(Book).all()
    data = []
    for book in books:
        data.append({
            "id": book.id,
            "work_key": book.work_key,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "description": book.description,
        })
    df = pd.DataFrame(data)
    return df