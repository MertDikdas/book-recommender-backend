from src.repositories import BookRepository, UserRepository
from src.domains.entities import BookEntity, CommentEntity
from src.uow.AbstractUOW import AbstractUnitOfWork

class BookService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    # Getting book by id service
    def get_book(self, book_id: int) -> BookEntity:
        with self.uow as uow:
            return uow.books.get_by_id(book_id)
    
    # Adding a new book service
    def create_book(self, title: str, author: str, description: str, genre: str, img_cover_url: str) -> BookEntity:
        with self.uow as uow:
            book = BookEntity(id=None, title=title, author=author, description=description, genre=genre, img_cover_url=img_cover_url)
            book = uow.books.add(book)
            uow.commit()
            return book
    
    # Listing all books service
    def list_all_books(self) -> list[BookEntity]:
        with self.uow as uow:
            return uow.books.list_all()
    
    # Getting book by title service
    def get_book_by_title(self, title: str) -> BookEntity:
        with self.uow as uow:
            return uow.books.get_by_title(title)
    
    # Searching books service
    def search_books(self, query: str) -> list[BookEntity]:
        with self.uow as uow:
            query = query.strip()
            if not query:
                # If query is empty, return all books or an empty list based on your preference
                return []
            return uow.books.search_books(query)
    
    def create_comment(self, book_id:int , username:str, comment_text:str) -> CommentEntity:
        with self.uow as uow:
            book = uow.books.get_by_id(book_id)
            if not book:
                return None
            user = uow.users.get_by_username(username)
            if not user:
                return None
            comment = uow.books.add_comment(book.id,user.id,comment_text)
            uow.commit()
            return comment
    
    def get_comments_by_book_id(self, book_id:int) -> list[CommentEntity]:
        with self.uow as uow:
            book = uow.books.get_by_id(book_id)
            if not book:
                return None
            comments = uow.books.get_comments_by_book_id(book_id)
            return comments
    
    def delete_comment_by_id(self, comment_id:int):
        with self.uow as uow:
            try:
                uow.books.delete_comment_by_id(comment_id)
                uow.commit()
            except ValueError as e:
                uow.rollback()
                raise Exception(status_code=404, detail=str(e))
            return