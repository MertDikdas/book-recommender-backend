from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.database import Base

class BookORM(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    work_key = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    genre = Column(String(255), nullable=True, index=True)   
    description = Column(Text)   
    img_cover_url = Column(String(255), nullable=True)

    ratings = relationship("RatingORM", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"

    
