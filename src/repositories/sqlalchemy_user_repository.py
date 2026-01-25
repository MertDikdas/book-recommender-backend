
from typing import Optional
from sqlalchemy.orm import Session
from src.domains.entities.user_entity import UserEntity
from src.repositories.user_repository import UserRepository
from src.domains.orm.user_orm import UserORM
from src.mappers.orm_to_entity_mapper import _user_orm_to_entity

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[UserEntity]:
        orm = self.db.query(UserORM).filter_by(username=username).first()
        return _user_orm_to_entity(orm) if orm else None

    def add(self, user: UserEntity) -> UserEntity:
        orm = UserORM(username=user.username)
        self.db.add(orm)
        self.db.flush()   # id oluşsun
        self.db.refresh(orm)
        self.db.commit()
        return _user_orm_to_entity(orm)