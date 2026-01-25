from typing import Optional
from src.domains.models import User as UserEntity
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, username: str) -> Optional[UserEntity]:
        existing = self.user_repo.get_by_username(username)
        if existing:
            return None

        user = UserEntity(id=None, username=username)
        return self.user_repo.add(user)
