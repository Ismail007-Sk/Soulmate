import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.soulmate_model import Soulmate


def create_soulmate(db: Session, data: dict) -> Soulmate:
    soulmate = Soulmate(**data)

    db.add(soulmate)
    db.commit()
    db.refresh(soulmate)

    return soulmate


def get_soulmate_by_user_id(
    db: Session,
    user_id: uuid.UUID,
) -> Soulmate | None:
    statement = select(Soulmate).where(
        Soulmate.user_id == user_id
    )
    return db.scalar(statement)


def update_soulmate(
    db: Session,
    soulmate: Soulmate,
    data: dict,
) -> Soulmate:
    for field, value in data.items():
        setattr(soulmate, field, value)

    db.commit()
    db.refresh(soulmate)

    return soulmate


def delete_soulmate(
    db: Session,
    soulmate: Soulmate,
) -> None:
    db.delete(soulmate)
    db.commit()
