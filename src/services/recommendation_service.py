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

    def get_recommendations_for_user(self, user_name: str, top_k: int = 20) -> list[BookEntity] | None:
        # Fetch user ratings
        user = self.user_repo.get_by_username(user_name)
        if not user:
            return None
        user_ratings = self.rating_repo.get_for_user(user.id)
        user_books = {}
        for rating in user_ratings:
            book_id = rating.book_id
            if self.book_repo.get_by_id(book_id) is None:
                continue
            user_books[rating.book_id] = self.book_repo.get_by_id(book_id)

        
        
        return recommend_for_user(user_ratings, user_books, top_k=top_k)
    
    def get_recommendations_for_user_by_genre(self, user_name: str, genre: str, top_k: int = 20) -> list[BookEntity] | None:
        # Fetch user ratings
        user = self.user_repo.get_by_username(user_name)
        if not user:
            return None
        user_ratings = self.rating_repo.get_for_user(user.id)
        user_books = {}
        for rating in user_ratings:
            book_id = rating.book_id
            book = self.book_repo.get_by_id(book_id)
            if book is None or book.genre.find(genre) == -1:
                continue
            user_books[rating.book_id] = book

        
        
        return recommend_for_user(user_ratings, user_books, top_k=top_k)