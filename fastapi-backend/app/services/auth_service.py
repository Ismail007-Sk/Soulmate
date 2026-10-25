import hashlib
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.lib.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.lib.security import verify_password

from app.repositories import (
    refresh_token_repository,
    user_repository,
)


def _hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def login_user(
    db: Session,
    *,
    email: str,
    password: str,
) -> dict[str, str]:
    user = user_repository.get_user_by_email(db, email)

    if user is None or not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    try:
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        payload = decode_token(
            refresh_token,
            expected_type="refresh",
        )

        expires_at = datetime.fromtimestamp(
            payload["exp"],
            tz=timezone.utc,
        )

        refresh_token_repository.create_refresh_token(
            db,
            user_id=user.id,
            token_hash=_hash_refresh_token(refresh_token),
            expires_at=expires_at,
        )

        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    except Exception:
        db.rollback()
        raise


def refresh_access_token(
    db: Session,
    refresh_token: str,
) -> dict[str, str]:
    try:
        payload = decode_token(
            refresh_token,
            expected_type="refresh",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        ) from exc

    token_hash = _hash_refresh_token(refresh_token)

    token_record = (
        refresh_token_repository.get_refresh_token_by_hash(
            db,
            token_hash,
        )
    )

    now = datetime.now(timezone.utc)

    if (
        token_record is None
        or token_record.revoked_at is not None
        or token_record.expires_at <= now
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh session is invalid or revoked",
        )

    try:
        user_id = uuid.UUID(payload["sub"])
    except (ValueError, TypeError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token subject",
        ) from exc

    if token_record.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh session",
        )

    access_token = create_access_token(user_id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def logout_user(
    db: Session,
    refresh_token: str,
) -> None:
    try:
        payload = decode_token(
            refresh_token,
            expected_type="refresh",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        ) from exc

    token_hash = _hash_refresh_token(refresh_token)

    token_record = (
        refresh_token_repository.get_refresh_token_by_hash(
            db,
            token_hash,
        )
    )

    if token_record is None or token_record.revoked_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh session not found or already revoked",
        )

    try:
        user_id = uuid.UUID(payload["sub"])
    except (ValueError, TypeError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token subject",
        ) from exc

    if token_record.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh session",
        )

    try:
        refresh_token_repository.revoke_refresh_token(
            db,
            token_record,
            revoked_at=datetime.now(timezone.utc),
        )

        db.commit()

    except Exception:
        db.rollback()
        raise
