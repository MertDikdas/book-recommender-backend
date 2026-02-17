
from scripts.fetch_openlibrary import fetch_subject, SUBJECTS, LIMIT_PER_SUBJECT, PER_REQUEST_LIMIT
from src.mappers.json_to_book import JsonToBookMapper
from src.database.database import SessionLocal
from src.domains.orm.book_orm import BookORM

def save_books_to_db(data):
    mapper = JsonToBookMapper(data)
    books_data = mapper.map()
    
    db = SessionLocal()
    for book_info in books_data:
        book = BookORM(
            work_key=book_info["work_key"],
            title=book_info["title"],
            author=book_info["authors"],
            genre=book_info["genre"],
            description=book_info["subjects"],
            img_cover_url=book_info["img_cover_url"]
        )
        existing = db.query(BookORM).filter_by(work_key=book_info["work_key"]).first()
        if existing:
            existing_genre = existing.genre
            if existing_genre and book.genre:
                combined_genres = existing_genre + "; " + book.genre
                existing.genre = combined_genres
            # print(f"Skipping existing book: {work_key}")
            continue
        db.add(book)
    db.commit()
    db.close()

if __name__ == "__main__":
    for subject in SUBJECTS:
        print(f"Fetching subject: {subject}")
        for offset in range(0, LIMIT_PER_SUBJECT, PER_REQUEST_LIMIT):
            data = fetch_subject(subject, PER_REQUEST_LIMIT, offset)
    
        save_books_to_db(data)
    print("Seeding completed.")