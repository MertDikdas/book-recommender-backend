from src.domains.entities import BookEntity
from src.recommender.tfidf_model import recommend_for_user
from src.uow.AbstractUOW import AbstractUnitOfWork
class RecommendationService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
    #Get recommendations for user for all books in user's library
    def get_recommendations_for_user(self, user_name: str, page_number:int, top_k: int = 20) -> list[BookEntity] | None:
        with self.uow as uow:
            # Fetch user ratings
            user = uow.users.get_by_username(user_name)
            if not user:
                return None
            user_ratings = uow.ratings.get_for_user(user.id)
            user_books = {}
            for rating in user_ratings:
                book_id = rating.book_id
                if uow.books.get_by_id(book_id) is None:
                    continue
                user_books[rating.book_id] = uow.books.get_by_id(book_id)

        
        
        return recommend_for_user(user_ratings, user_books, min_k=(page_number-1)*top_k, max_k=page_number*top_k)
    #Get  recommendations based on a specific genre which user has book in this genre
    def get_recommendations_for_user_by_genre(self, user_name: str, genre: str, page_number: int , top_k: int = 20) -> list[BookEntity] | None:
        with self.uow as uow:
            # Fetch user ratings
            user = uow.users.get_by_username(user_name)
            if not user:
                return None
            user_ratings = uow.ratings.get_for_user(user.id)
            genre_user_ratings = []
            user_books = {}
            for rating in user_ratings:
                book_id = rating.book_id
                book = uow.books.get_by_id(book_id)
                if book is None or book.genre.find(genre) == -1:
                    continue
                genre_user_ratings.append(rating)
                user_books[rating.book_id] = book
            return recommend_for_user(genre_user_ratings, user_books, min_k=(page_number-1)*top_k, max_k=page_number*top_k)