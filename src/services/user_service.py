from typing import Optional
from src.domains.entities.user_entity import UserEntity
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.rating_repository import RatingRepository
from src.domains.entities.book_entity import BookEntity
from typing import Iterable
from src.uow.AbstractUOW import AbstractUnitOfWork

class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
    #Create user
    def create_user(self, username: str) -> Optional[UserEntity]:
        with self.uow as uow:
            existing = uow.users.get_by_username(username)
            if existing:
                return None

            user = UserEntity(id=None, username=username)
            user = uow.users.add(user)
            uow.commit()
            return user
    #Get user by username
    def get_user(self, username: str) -> Optional[UserEntity]:
        with self.uow as uow:
            return uow.users.get_by_username(username)
    
    # Getting books by user service
    def get_user_books(self, username: str) -> Iterable[BookEntity]:
        with self.uow as uow:
            user = uow.users.get_by_username(username)  # Ensure user exists, can raise exception if not found
            if not user:
                raise ValueError(f"User with username '{username}' not found")
            user_id = user.id
            ratings = uow.ratings.get_for_user(user_id)
            if ratings is None:
                return []
            for rating in ratings:
                book = uow.books.get_by_id(rating.book_id)
                if book:
                    yield book
    #Delete user by username
    def delete_user(self, username: str) -> None:
        with self.uow as uow:
            user = uow.users.get_by_username(username)
            if not user:
                raise ValueError(f"User with username '{username}' not found")
            uow.users.delete(username)
            uow.commit()

    #Get user's genres
    def get_user_genres(self, username: str) -> Iterable[str]:
        with self.uow as uow:
            user = uow.users.get_by_username(username)  # Ensure user exists, can raise exception if not found
            if not user:
                raise ValueError(f"User with username '{username}' not found")
            user_id = user.id
            ratings = uow.ratings.get_for_user(user_id)
            if ratings is None:
                return []
            genres = set()
            for rating in ratings:
                book = uow.books.get_by_id(rating.book_id)
                if book and book.genre:
                    genres.update(genre.strip() for genre in book.genre.split(";"))
            return genres
    
    #Get user by id
    def get_user_by_id(self, user_id:int) -> Optional[UserEntity]:
        with self.uow as uow:
            user = uow.users.get_by_id(user_id)
            return user