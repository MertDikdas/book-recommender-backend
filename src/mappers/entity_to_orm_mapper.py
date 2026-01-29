from src.domains.entities import UserEntity, BookEntity, RatingEntity
from src.domains.orm import UserORM, BookORM, RatingORM

def user_entity_to_orm(entity: UserEntity) -> UserORM:
    orm = UserORM(
        id=entity.id,
        username=entity.username
    )
    return orm

def book_entity_to_orm(entity: BookEntity) -> BookORM:
    orm = BookORM(
        id = entity.id,
        title = entity.title,
        work_key = entity.work_key,
        author = entity.author,
        description = entity.description,
        genre = entity.genre
    )
    return orm

def rating_entity_to_orm(entity: RatingEntity) -> RatingORM:
    orm = RatingORM(
        id= entity.id,
        book_id = entity.book_id,
        user_id = entity.user_id,
        value = entity.value
    )
    return orm
