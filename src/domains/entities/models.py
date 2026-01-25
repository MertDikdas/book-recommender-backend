from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    username: str


@dataclass
class Book:
    id: Optional[int]
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Rating:
    id: Optional[int]
    user_id: int
    book_id: int
    value: int