import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users_model import User


def create_user(db: Session, data: dict[str, Any]) -> User:
    user = User(**data)     #user = User(name="Bob", email="bob@gmail.com", age=30)

    db.add(user)
    db.flush()
    db.refresh(user)

    return user


def get_all_users(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    statement = select(User).offset(skip).limit(limit)

    return list(db.scalars(statement).all())


def get_user_by_id(
    db: Session,
    user_id: uuid.UUID,
) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return db.scalar(statement)


def update_user(
    db: Session,
    user: User,
    data: dict[str, Any],
) -> User:
    for field, value in data.items():
        setattr(user, field, value)

    db.flush()
    db.refresh(user)

    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.flush()
