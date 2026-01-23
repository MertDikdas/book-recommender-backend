from scripts.database import SessionLocal
from scripts.models import User, Book, Rating

def main():
    db = SessionLocal()

    # Create a new user
    new_user = User(username="testuser")
    db.add(new_user)

    # Create a new book
    new_book = Book(title="Test Book", 
                    author="Author Name", 
                    genre="Fiction", 
                    description="A test book description.")
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.refresh(new_user)
    # Create a new rating
    new_rating = Rating(user_id=new_user.id, book_id=new_book.id, rating=5)
    db.add(new_rating)
    db.commit()
    u = db.query(User).filter_by(username="testuser").first()
    print("User:", u.username)
    for r in u.ratings:
        print("Rating:", r.rating, "Book:", r.book.title)


    db.close()
if __name__ == "__main__":
    main()