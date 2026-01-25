from dataclasses import dataclass
from typing import Optional

@dataclass
class BookEntity:
    id: Optional[int]
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None