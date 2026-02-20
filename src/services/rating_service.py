# src/domain/services.py
from src.domains.entities.rating_entity import RatingEntity
from src.repositories.rating_repository import RatingRepository
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.uow.AbstractUOW import AbstractUnitOfWork

class RatingService:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow=uow

    # Create or update rating
    def rate_book(self, username: str, book_id: int, value: int) -> RatingEntity:
        with self.uow as uow:
            if value < 0 or value > 5:
                raise ValueError("Rating must be between 1 and 5")

            # 1) find the user if not exist raise error
            user = self.uow.users.get_by_username(username)
            if user is None:
                raise ValueError(f"User {username} could not be found")

            # 2) find the book if not exist raise error
            book = self.uow.books.get_by_id(book_id)
            if book is None:
                raise ValueError(f"Book id={book_id} not found")

            # 3) check existing rating -> update / create
            existing = self.uow.ratings.get_for_user_and_book(user.id, book_id)
            if existing:
                existing.value = value
                return self.uow.ratings.update(existing)

            rating = RatingEntity(id=None, user_id=user.id, book_id=book_id, rating=value)
            return self.uow.ratings.add(rating)
    
    # Get rating for user and book
    def get_rating_for_user_and_book(self, username: str, book_id: int) -> RatingEntity:
        with self.uow as uow:
            # 1) find the user if not exist raise error
            user = self.uow.users.get_by_username(username)
            if user is None:
                return None

            # 2) find the book if not exist raise error
            book = self.uow.books.get_by_id(book_id)
            if book is None:
                return None

            # 3) get rating
            rating = self.uow.ratings.get_for_user_and_book(user.id, book_id)
            return rating
    
    # Get ratings for user
    def get_ratings_for_user(self, username: str) -> list[RatingEntity]:
        with self.uow as uow:
            # 1) find the user if not exist raise error
            user = self.uow.users.get_by_username(username)
            if user is None:
                return []

            # 2) get ratings
            ratings = self.uow.ratings.get_for_user(user.id)
            return ratings
    
    def delete_user_book(self, username: str, book_id: int) -> bool:
        with self.uow as uow:
            user = self.uow.users.get_by_username(username)
            if not user:
                raise ValueError(f"User with username '{username}' not found")
            user_id = user.id
            rating = self.uow.ratings.get_for_user_and_book(user_id, book_id)
            if not rating:
                return False  # No rating means the user doesn't have this book in their list
            self.uow.ratings.delete(rating.id)
            uow.commit()
            return True