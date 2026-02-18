from typing import Optional
from src.domains.entities.user_entity import UserEntity
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.rating_repository import RatingRepository
from src.domains.entities.book_entity import BookEntity
from typing import Iterable


class UserService:
    def __init__(self, user_repo: UserRepository, book_repo: BookRepository, rating_repo: RatingRepository):
        self.user_repo = user_repo
        self.book_repo = book_repo
        self.rating_repo = rating_repo

    def create_user(self, username: str) -> Optional[UserEntity]:
        existing = self.user_repo.get_by_username(username)
        if existing:
            return None

        user = UserEntity(id=None, username=username)
        user = self.user_repo.add(user)
        return user

    def get_user(self, username: str) -> Optional[UserEntity]:
        return self.user_repo.get_by_username(username)
    
    # Getting books by user service
    def get_user_books(self, username: str) -> Iterable[BookEntity]:
        user = self.user_repo.get_by_username(username)  # Ensure user exists, can raise exception if not found
        if not user:
            raise ValueError(f"User with username '{username}' not found")
        user_id = user.id
        ratings = self.rating_repo.get_for_user(user_id)
        if ratings is None:
            return []
        for rating in ratings:
            book = self.book_repo.get_by_id(rating.book_id)
            if book:
                yield book
    
    def delete_user(self, username: str) -> None:
        user = self.user_repo.get_by_username(username)
        if not user:
            raise ValueError(f"User with username '{username}' not found")
        self.user_repo.delete(username)

    def get_user_genres(self, username: str) -> Iterable[str]:
        user = self.user_repo.get_by_username(username)  # Ensure user exists, can raise exception if not found
        if not user:
            raise ValueError(f"User with username '{username}' not found")
        user_id = user.id
        ratings = self.rating_repo.get_for_user(user_id)
        if ratings is None:
            return []
        genres = set()
        for rating in ratings:
            book = self.book_repo.get_by_id(rating.book_id)
            if book and book.genre:
                genres.update(genre.strip() for genre in book.genre.split(";"))
        return genres
    
    def get_user_by_id(self, user_id:int) -> Optional[UserEntity]:
        user = self.user_repo.get_by_id(user_id)
        return user