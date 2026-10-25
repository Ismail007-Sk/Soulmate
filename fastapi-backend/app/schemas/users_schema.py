import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import re
from app.models.users_model import Gender, UserRole

# 1. Shared password validation helper
def validate_password_strength(v: str | None) -> str | None:
    if v is None:
        return v
    if not re.search(r"[A-Z]", v):
        raise ValueError("Must contain at least one uppercase letter (A-Z)")
    if not re.search(r"[a-z]", v):
        raise ValueError("Must contain at least one lowercase letter (a-z)")
    if not re.search(r"\d", v):
        raise ValueError("Must contain at least one number (0-9)")
    if not re.search(r"[@$!%*?&._-]", v):
        raise ValueError("Must contain at least one special character (@$!%*?&)")
    return v


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    gender: Gender
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    gender: Gender | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    gender: Gender
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)