from src.domains.entities import UserEntity, BookEntity, RatingEntity
from src.domains.orm import UserORM, BookORM, RatingORM

def _user_orm_to_entity(orm: UserORM) -> UserEntity:
    return UserEntity(id=orm.id, username=orm.username)


def _book_orm_to_entity(orm: BookORM) -> BookEntity:
    return BookEntity(
        id=orm.id,
        title=orm.title,
        author=orm.author,
        genre=orm.genre,
        description=orm.description,
    )


def _rating_orm_to_entity(orm: RatingORM) -> RatingEntity:
    return RatingEntity(
        id=orm.id,
        user_id=orm.user_id,
        book_id=orm.book_id,
        rating=orm.rating,
    )