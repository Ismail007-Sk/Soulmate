import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

from app.config.settings import settings


def create_access_token(user_id: uuid.UUID | str) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: uuid.UUID | str) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(
    token: str,
    expected_type: str,
) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "require": ["sub", "exp", "iat", "type"],
            },
        )

    except InvalidTokenError as exc:
        raise ValueError("Invalid or expired token") from exc

    if payload.get("type") != expected_type:
        raise ValueError("Incorrect token type")

    try:
        uuid.UUID(payload["sub"])
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError("Invalid token subject") from exc

    return payload
