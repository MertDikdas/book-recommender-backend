from src.repositories import BookRepository, UserRepository
from src.domains.entities import BookEntity, UserEntity, CommentEntity

class BookService:
    def __init__(self, book_repo: BookRepository, user_repo: UserRepository):
        self.book_repo = book_repo
        self.user_repo = user_repo

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
    
    def create_comment(self, book_id:int , username:str, comment_text:str) -> CommentEntity:
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return None
        user = self.user_repo.get_by_username(username)
        if not user:
            return None
        comment = self.book_repo.add_comment(book.id,user.id,comment_text)
        return comment
    
    def get_comments_by_book_id(self, book_id:int) -> list[CommentEntity]:
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return None
        comments = self.book_repo.get_comments_by_book_id(book_id)
        return comments
    
    def delete_comment_by_id(self, comment_id:int):
        try:
            self.book_repo.delete_comment_by_id(comment_id)
        except ValueError as e:
            raise Exception(status_code=404, detail=str(e))
        return