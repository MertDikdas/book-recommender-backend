# src/domain/services.py
from ..domains.models import User, Rating
from ..repositories.rating_repository import RatingRepository
from ..repositories.user_repository import UserRepository
from ..repositories.book_repository import BookRepository

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

    def rate_book(self, username: str, book_id: int, value: int) -> Rating:
        if value < 1 or value > 5:
            raise ValueError("Rating 1 ile 5 arasında olmalı")

        # 1) kullanıcıyı bul / oluştur
        user = self.user_repo.get_by_username(username)
        if user is None:
            user = User(id=None, username=username)
            user = self.user_repo.add(user)

        # 2) kitap var mı?
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            raise ValueError(f"Book id={book_id} bulunamadı")

        # 3) daha önce rating var mı? -> update / yoksa -> create
        existing = self.rating_repo.get_for_user_and_book(user.id, book_id)
        if existing:
            existing.value = value
            return self.rating_repo.update(existing)

        rating = Rating(id=None, user_id=user.id, book_id=book_id, value=value)
        return self.rating_repo.add(rating)
