from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.database import Base

class CommentORM(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    comment_text = Column(Text)

    user = relationship("UserORM", back_populates="comments")
    book = relationship("BookORM", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, comment_text={self.rating})>"