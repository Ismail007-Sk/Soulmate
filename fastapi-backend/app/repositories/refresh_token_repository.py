import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.refresh_token_model import RefreshToken


def create_refresh_token(
    db: Session,
    *,
    user_id: uuid.UUID,
    token_hash: str,
    expires_at: datetime,
) -> RefreshToken:
    token_record = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(token_record)
    db.flush()
    db.refresh(token_record)

    return token_record

def get_refresh_token_by_hash(
    db: Session,
    token_hash: str,
) -> RefreshToken | None:
    statement = select(RefreshToken).where(
        RefreshToken.token_hash == token_hash
    )

    return db.scalar(statement)

def revoke_refresh_token(
    db: Session,
    token_record: RefreshToken,
    *,
    revoked_at: datetime,
) -> RefreshToken:
    token_record.revoked_at = revoked_at

    db.flush()
    db.refresh(token_record)

    return token_record

# nuclear option-> Log Out of All Devices, Password Changes etc
def revoke_all_user_refresh_tokens(
    db: Session,
    user_id: uuid.UUID,
    *,
    revoked_at: datetime,
) -> int:
    statement = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None),
    )

    token_records = db.scalars(statement).all()

    for token_record in token_records:
        token_record.revoked_at = revoked_at

    db.flush()

    return len(token_records)
