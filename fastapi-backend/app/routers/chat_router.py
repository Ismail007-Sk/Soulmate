
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.db_dependency import get_db
from app.models.users_model import User
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import chat_with_soulmate

chatRouter = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@chatRouter.post("/", response_model=ChatResponse)
async def chat_endpoint(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reply = await chat_with_soulmate(
        db=db,
        user_id=current_user.id,
        message=data.message,
    )

    return ChatResponse(reply=reply)
