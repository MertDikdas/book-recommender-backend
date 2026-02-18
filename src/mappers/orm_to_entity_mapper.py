from src.domains.entities import UserEntity, BookEntity, RatingEntity, CommentEntity
from src.domains.orm import UserORM, BookORM, RatingORM, CommentORM

def _user_orm_to_entity(orm: UserORM) -> UserEntity:
    return UserEntity(id=orm.id, username=orm.username)


def _book_orm_to_entity(orm: BookORM) -> BookEntity:
    return BookEntity(
        id=orm.id,
        title=orm.title,
        work_key=orm.work_key,
        author=orm.author,
        genre=orm.genre,
        description=orm.description,
        img_cover_url=orm.img_cover_url,
        comments=[_comment_orm_to_entity(comment) for comment in (orm.comments or [])]
    )

def _comment_orm_to_entity(orm: CommentORM) -> CommentEntity:
    return CommentEntity(
        id=orm.id,
        book_id=orm.book_id,
        user_id=orm.user_id,
        comment_text=orm.comment_text
    )

def _rating_orm_to_entity(orm: RatingORM) -> RatingEntity:
    return RatingEntity(
        id=orm.id,
        user_id=orm.user_id,
        book_id=orm.book_id,
        rating=orm.rating,
    )