from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.db_dependency import get_db
from app.models.users_model import User
from app.schemas.soulmate_schema import (
    SoulmateCreate,
    SoulmateResponse,
    SoulmateUpdate,
)
from app.services.soulmate_service import (
    create_soulmate,
    delete_my_soulmate,
    get_my_soulmate,
    update_my_soulmate,
)

soulRouter = APIRouter(
    prefix="/soulmates",
    tags=["Soulmates"],
)


@soulRouter.post(
    "/",
    response_model=SoulmateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_soulmate_endpoint(
    data: SoulmateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_soulmate(
        db=db,
        user_id=current_user.id,
        data=data,
    )


@soulRouter.get(
    "/me",
    response_model=SoulmateResponse,
)
def get_my_soulmate_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_soulmate(
        db=db,
        user_id=current_user.id,
    )


@soulRouter.patch(
    "/me",
    response_model=SoulmateResponse,
)
def update_my_soulmate_endpoint(
    data: SoulmateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_my_soulmate(
        db=db,
        user_id=current_user.id,
        data=data,
    )


@soulRouter.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_soulmate_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_my_soulmate(
        db=db,
        user_id=current_user.id,
    )
