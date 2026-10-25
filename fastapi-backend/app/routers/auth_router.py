
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.schemas.auth_schema import (
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    TokenResponse,
)
from app.schemas.users_schema import UserCreate, UserResponse
from app.services import auth_service, user_service


authRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@authRouter.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(db, data)


@authRouter.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    return auth_service.login_user(
        db,
        email=str(data.email),
        password=data.password,
    )


@authRouter.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    data: RefreshRequest,
    db: Session = Depends(get_db),
):
    return auth_service.refresh_access_token(
        db,
        refresh_token=data.refresh_token,
    )


@authRouter.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    data: RefreshRequest,
    db: Session = Depends(get_db),
):
    auth_service.logout_user(
        db,
        refresh_token=data.refresh_token,
    )

    return {"message": "Logged out successfully"}
