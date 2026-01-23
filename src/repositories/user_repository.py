from abc import ABC, abstractmethod
from typing import Optional
from ..domains.models import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: ...
    
    @abstractmethod
    def add(self, user: User) -> User: ...