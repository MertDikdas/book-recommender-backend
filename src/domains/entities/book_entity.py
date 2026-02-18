from dataclasses import dataclass, field
from typing import Optional
from src.domains.entities.comment_entity import CommentEntity

@dataclass
class BookEntity:
    id: Optional[int]
    title: str
    work_key: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    img_cover_url: Optional[str] = None

    comments: list[CommentEntity] = field(default_factory=list)