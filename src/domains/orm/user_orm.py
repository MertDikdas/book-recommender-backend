from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.database import Base

class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)

    ratings = relationship("RatingORM", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    