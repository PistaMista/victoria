from fastapi import status, HTTPException, APIRouter, Depends, Body
from app.services.chat import (
    ChatService,
    NonexistentMessageError,
    QueryAlreadyAnsweredError,
)
from app.model.user import User
from app.containers import Container
from dependency_injector.wiring import inject, Provide
from .dependencies.auth import get_non_admin_user
from typing import Annotated, Optional, Any

router = APIRouter()


@router.get("/{id}/answer", response_model=Optional[str])
@inject
async def get_query_answer(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])],
) -> Optional[str]:
    try:
        answer = chat_service.get_user_query_answer(user_id=user.id, message_id=id)
        return answer
    except NonexistentMessageError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/{id}/answer")
@inject
async def set_query_answer(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])],
    body: Any = Body(..., media_type="application/json"),
):
    try:
        chat_service.set_user_query_answer(user_id=user.id, message_id=id, answer=body)
    except QueryAlreadyAnsweredError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except NonexistentMessageError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
