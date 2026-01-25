from dataclasses import dataclass
from typing import Optional

@dataclass
class RatingEntity:
    id: Optional[int]
    user_id: int
    book_id: int
    value: int