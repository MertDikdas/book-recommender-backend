import requests
from scripts.fetch_openlibrary import fetch_subject, SUBJECTS, LIMIT_PER_SUBJECT
from scripts.mapper.json_to_book import JsonToBookMapper
from scripts.database import SessionLocal
from scripts.models import Book

def save_books_to_db(data):
    mapper = JsonToBookMapper(data)
    books_data = mapper.map()
    
    db = SessionLocal()
    for book_info in books_data:
        book = Book(
            work_key=book_info["work_key"],
            title=book_info["title"],
            author=book_info["authors"],
            genre=book_info["genre"],
            description=book_info["subjects"]
        )
        existing = db.query(Book).filter_by(work_key=book_info["work_key"]).first()
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
        data = fetch_subject(subject, LIMIT_PER_SUBJECT)
        save_books_to_db(data)
    print("Seeding completed.")