import uuid
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.soulmate_repository import (
    create_soulmate as create_soulmate_repository,
    delete_soulmate as delete_soulmate_repository,
    get_soulmate_by_user_id,
    update_soulmate as update_soulmate_repository,
)
from app.schemas.soulmate_schema import SoulmateCreate, SoulmateUpdate


def create_soulmate(
    db: Session,
    user_id: uuid.UUID,
    data: SoulmateCreate,
):
    existing_soulmate = get_soulmate_by_user_id(db, user_id)

    if existing_soulmate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Soulmate already exists for this user.",
        )

    try:
        return create_soulmate_repository(
            db=db,
            data={
                **data.model_dump(),
                "user_id": user_id,
            },
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Soulmate could not be created. Please try again.",
        ) from exc


def get_my_soulmate(
    db: Session,
    user_id: uuid.UUID,
):
    soulmate = get_soulmate_by_user_id(db, user_id)

    if soulmate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soulmate not found.",
        )

    return soulmate


def update_my_soulmate(
    db: Session,
    user_id: uuid.UUID,
    data: SoulmateUpdate,
):
    soulmate = get_soulmate_by_user_id(db, user_id)

    if soulmate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soulmate not found.",
        )

    try:
        return update_soulmate_repository(
            db=db,
            soulmate=soulmate,
            data=data.model_dump(exclude_unset=True),
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Soulmate could not be updated. Please try again.",
        ) from exc


def delete_my_soulmate(
    db: Session,
    user_id: uuid.UUID,
) -> None:
    soulmate = get_soulmate_by_user_id(db, user_id)

    if soulmate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soulmate not found.",
        )

    delete_soulmate_repository(
        db=db,
        soulmate=soulmate,
    )
