from src.repositories.book_repository import BookRepository
from src.domains.entities.book_entity import BookEntity

class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    # Getting book by id service
    def get_book(self, book_id: int) -> BookEntity:
        return self.book_repo.get_by_id(book_id)
    
    # Adding a new book service
    def create_book(self, title: str, author: str, description: str, genre: str, img_cover_url: str) -> BookEntity:
        book = BookEntity(id=None, title=title, author=author, description=description, genre=genre, img_cover_url=img_cover_url)
        book = self.book_repo.add(book)
        return book
    
    # Listing all books service
    def list_books(self) -> list[BookEntity]:
        return self.book_repo.list_all()
    
    # Getting book by title service
    def get_book_by_title(self, title: str) -> BookEntity:
        return self.book_repo.get_by_title(title)
    
    # Searching books service
    def search_books(self, query: str) -> list[BookEntity]:
        query = query.strip()
        if not query:
            # If query is empty, return all books or an empty list based on your preference
            return []
        return self.book_repo.search_books(query)
    
