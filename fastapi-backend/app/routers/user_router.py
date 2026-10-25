import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import (
    get_current_user,
    require_roles,
)
from app.dependencies.db_dependency import get_db
from app.models.users_model import User, UserRole
from app.schemas.auth_schema import MessageResponse
from app.schemas.users_schema import UserResponse, UserUpdate
from app.services import user_service


userRouter = APIRouter(prefix="/users", tags=["Users"])

CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[
    User,
    Depends(require_roles(UserRole.ADMIN)),
]
DatabaseSession = Annotated[Session, Depends(get_db)]


# Any authenticated user can update their own profile.
@userRouter.patch("/me", response_model=UserResponse)
def update_my_profile(
    data: UserUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    return user_service.update_user(
        db,
        current_user.id,
        data,
    )


# Admin only: retrieve all users.
@userRouter.get("/", response_model=list[UserResponse])
def get_all_users(
    current_user: AdminUser,
    db: DatabaseSession,
    skip: int = 0,
    limit: int = 100,
):
    return user_service.get_all_users(
        db,
        skip=skip,
        limit=limit,
    )


# Admin only: retrieve a specific user.
@userRouter.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: uuid.UUID,
    current_user: AdminUser,
    db: DatabaseSession,
):
    return user_service.get_user_by_id(
        db,
        user_id,
    )


# Admin only: delete a specific user.
@userRouter.delete(
    "/{user_id}",
    response_model=MessageResponse,
)
def delete_user(
    user_id: uuid.UUID,
    current_user: AdminUser,
    db: DatabaseSession,
):
    user_service.delete_user(db, user_id)

    return {"message": "User deleted successfully"}
