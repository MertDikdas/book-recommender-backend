from sqlalchemy.orm import Session
from src.domains.orm import BookORM
import pandas as pd

def pull_books_from_db(db: Session) -> pd.DataFrame:
    books = db.query(BookORM).all()
    data = []
    for book in books:
        data.append({
            "id": book.id,
            "work_key": book.work_key,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "description": book.description,
            "img_cover_url": book.img_cover_url
        })
    df = pd.DataFrame(data)
    return df