import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.lib.security import hash_password
from app.models.users_model import User
from app.repositories import user_repository
from app.schemas.users_schema import UserCreate, UserUpdate


def create_user(db: Session, data: UserCreate) -> User:
    existing_user = user_repository.get_user_by_email(
        db,
        str(data.email),
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    user_data = {
        "name": data.name,
        "gender": data.gender,
        "email": str(data.email),
        "password_hash": hash_password(data.password),
        # "role":"admin",
    }

    try:
        user = user_repository.create_user(db, user_data)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from exc

    except Exception:
        db.rollback()
        raise

def get_all_users(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skip cannot be negative",
        )

    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100",
        )

    return user_repository.get_all_users(
        db,
        skip=skip,
        limit=limit,
    )

def get_user_by_id(
    db: Session,
    user_id: uuid.UUID,
) -> User:
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

def update_user(
    db: Session,
    user_id: uuid.UUID,
    data: UserUpdate,
) -> User:
    user = get_user_by_id(db, user_id)

    # Grab only the fields the client actually sent
    updates = data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    # 1. Handle password specially (hash it if provided, drop it if null)
    if "password" in updates:
        password = updates.pop("password")
        if password is not None:
            updates["password_hash"] = hash_password(password)

    # 2. Filter out ANY remaining field that was sent as null/None
    updates = {k: v for k, v in updates.items() if v is not None}

    # 3. Check again if anything is left to update
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update",
        )

    try:
        updated_user = user_repository.update_user(
            db,
            user,
            updates,
        )

        db.commit()
        db.refresh(updated_user)

        return updated_user

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User update conflicts with existing data",
        ) from exc

    except Exception:
        db.rollback()
        raise

def delete_user(
    db: Session,
    user_id: uuid.UUID,
) -> User:
    user = get_user_by_id(db, user_id)

    try:
        user_repository.delete_user(db, user)
        db.commit()

        return user

    except Exception:
        db.rollback()
        raise
