
from src.api.open_library_api.fetch_openlibrary import fetch_subject, SUBJECTS, LIMIT_PER_SUBJECT, PER_REQUEST_LIMIT, fetch_tr_books
import time
from src.mappers.json_to_book import JsonToBookMapper
from src.database.database import SessionLocal
from src.domains.orm.book_orm import BookORM

def save_books_to_db(data,works):
    mapper = JsonToBookMapper(data)
    books_data = mapper.map(works)
    
    db = SessionLocal()
    for book_info in books_data:

        book = BookORM(
            work_key=book_info["work_key"],
            title=book_info["title"],
            author=book_info["authors"],
            genre=book_info["genre"],
            description=book_info["description"],
            img_cover_url=book_info["img_cover_url"]
        )
        existing = db.query(BookORM).filter_by(work_key=book_info["work_key"]).first()
        if existing:
            existing_genre = existing.genre
            if existing_genre and book.genre and book.genre.find(existing_genre)==-1:
                combined_genres = existing_genre + "; " + book.genre
                existing.genre = combined_genres
            # print(f"Skipping existing book: {work_key}")
            continue
        db.add(book)
    db.commit()
    db.close()

if __name__ == "__main__":
    #FOR ENGLISH BOOKS
    for subject in SUBJECTS:
        print(f"Fetching subject: {subject}")
        for offset in range(0, LIMIT_PER_SUBJECT, PER_REQUEST_LIMIT):
           data = fetch_subject(subject, PER_REQUEST_LIMIT, offset)
           save_books_to_db(data,"works")
    #FOR TURKISH BOOKS 
    for page in range(1, 51):  # 50 sayfa * 100 = 5000 kitap
        data = fetch_tr_books(query="subject:literature language:tur", page=page, limit=100)
        save_books_to_db(data,"docs");
        print("page", page, "docs", len(data))
        time.sleep(0.2)

    print("Seeding completed.")