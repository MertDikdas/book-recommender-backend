from src.domains.entities import RatingEntity, BookEntity, UserEntity
from src.repositories import RatingRepository , UserRepository, BookRepository
from src.recommender.tfidf_model import recommend_for_user

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

    def get_recommendations_for_user(self, user_id: int) -> list[BookEntity]:
        # Fetch user ratings
        user_ratings = self.rating_repo.get_for_user(user_id)

        return recommend_for_user(user_ratings)