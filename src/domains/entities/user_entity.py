from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    id: Optional[int]
    username: str


