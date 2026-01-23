from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from scripts.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)

    ratings = relationship("Rating", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"