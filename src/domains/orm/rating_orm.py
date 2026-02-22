from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.database import Base

class RatingORM(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # Assuming rating is an integer value
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserORM", back_populates="ratings")
    book = relationship("BookORM", back_populates="ratings")

    def __repr__(self):
        return f"<Rating(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, rating={self.rating})>"