from src.repositories.book_repository import BookRepository
from src.domains.entities.book_entity import BookEntity


class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo
    
    def get_book(self, book_id: int) -> BookEntity:
        return self.book_repo.get_by_id(book_id)
    
    def create_book(self, title: str, author: str, description: str, genre: str) -> BookEntity:
        book = BookEntity(id=None, title=title, author=author, description=description, genre=genre)
        book = self.book_repo.add(book)
        return book
    
    def list_books(self) -> list[BookEntity]:
        return self.book_repo.list_all()
    
    def get_book_by_title(self, title: str) -> BookEntity:
        return self.book_repo.get_by_title(title)
        