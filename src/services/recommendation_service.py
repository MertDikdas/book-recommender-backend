from src.domains.entities import RatingEntity, BookEntity, UserEntity
from src.repositories.rating_repository import RatingRepository , UserRepository, BookRepository


class RecommendationService:
    def __init__(
        self,
        user_repo: UserRepository,
        book_repo: BookRepository,
        rating_repo: RatingRepository,
    ):
        self.user_repo = user_repo
        self.book_repo = book_repo
        self.rating_repo = rating_repo