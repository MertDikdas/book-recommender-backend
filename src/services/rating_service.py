# src/domain/services.py
from src.domains.entities.rating_entity import RatingEntity
from src.repositories.rating_repository import RatingRepository
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository

class RatingService:
    def __init__(
        self,
        user_repo: UserRepository,
        book_repo: BookRepository,
        rating_repo: RatingRepository,
    ):
        self.user_repo = user_repo
        self.book_repo = book_repo
        self.rating_repo = rating_repo
    # Create or update rating
    def rate_book(self, username: str, book_id: int, value: int) -> RatingEntity:
        if value < 0 or value > 5:
            raise ValueError("Rating must be between 1 and 5")

        # 1) find the user if not exist raise error
        user = self.user_repo.get_by_username(username)
        if user is None:
            raise ValueError(f"User {username} could not be found")

        # 2) find the book if not exist raise error
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            raise ValueError(f"Book id={book_id} not found")

        # 3) check existing rating -> update / create
        existing = self.rating_repo.get_for_user_and_book(user.id, book_id)
        if existing:
            existing.value = value
            return self.rating_repo.update(existing)

        rating = RatingEntity(id=None, user_id=user.id, book_id=book_id, rating=value)
        return self.rating_repo.add(rating)
    
    # Get rating for user and book
    def get_rating_for_user_and_book(self, username: str, book_id: int) -> RatingEntity:
        # 1) find the user if not exist raise error
        user = self.user_repo.get_by_username(username)
        if user is None:
            return None

        # 2) find the book if not exist raise error
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            return None

        # 3) get rating
        rating = self.rating_repo.get_for_user_and_book(user.id, book_id)
        return rating
    
    # Get ratings for user
    def get_ratings_for_user(self, username: str) -> list[RatingEntity]:
        # 1) find the user if not exist raise error
        user = self.user_repo.get_by_username(username)
        if user is None:
            return []

        # 2) get ratings
        ratings = self.rating_repo.get_for_user(user.id)
        return ratings