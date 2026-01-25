from typing import Optional
from src.domains.entities.user_entity import UserEntity
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, username: str) -> Optional[UserEntity]:
        existing = self.user_repo.get_by_username(username)
        if existing:
            return None

        user = UserEntity(id=None, username=username)
        user = self.user_repo.add(user)
        return user

    def get_user(self, username: str) -> Optional[UserEntity]:
        return self.user_repo.get_by_username(username)