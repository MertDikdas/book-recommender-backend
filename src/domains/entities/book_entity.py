from dataclasses import dataclass
from typing import Optional

@dataclass
class BookEntity:
    id: Optional[int]
    title: str
    work_key: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None