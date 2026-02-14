from abc import ABC, abstractmethod
from typing import Optional
from ..domains.entities.user_entity import UserEntity

class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserEntity]: ...
    
    @abstractmethod
    def add(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]: ...

    @abstractmethod
    def delete(self, user_id: int) -> None: ...
