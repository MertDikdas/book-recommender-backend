from dataclasses import dataclass
from typing import Optional

@dataclass
class CommentEntity:
    id: Optional[int]
    user_id: int
    book_id: int
    comment_text: str