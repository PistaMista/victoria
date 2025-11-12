from fastapi import status, APIRouter, HTTPException, Depends, Request
from app.services.chat import ChatService, NonexistentExchangeError
from .schema.messages import SendMessage, SendMessageMarkdown, SendMessageChoicePrompt, MessageResponse, to_message_response, RepliedChoiceInfoResponse
from .dependencies.auth import get_non_admin_user
from app.model.user import User
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from typing import List, Annotated, Union
import time

router = APIRouter()

@router.get("/{id}/messages", response_model=List[MessageResponse])
@inject
async def get_messages_long_poll(
    id: int,
    after: int,
    request: Request,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> List[MessageResponse]:
    try:
        running = 0.0
        timeout = 2.5
        interval = 0.5
        while not await request.is_disconnected() and not running > timeout:
            new = chat_service.get_user_exchange_replies_after(
                user_id=user.id,
                exchange_id=id,
                after=after
            )

            if new:
                return [to_message_response(x) for x in new]

            time.sleep(interval)
            running += interval

        return []
    except NonexistentExchangeError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.post("/{id}/send-reply", response_model=Union[RepliedChoiceInfoResponse, None])
@inject
async def send_reply_to_exchange(
    id: int,
    msg: SendMessage,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> Union[RepliedChoiceInfoResponse, None]:
    try:
        if isinstance(msg, SendMessageMarkdown):
            chat_service.send_markdown_reply_to_user_exchange(
                user_id=user.id,
                exchange_id=id,
                from_agent_id=msg.fromAgentId,
                markdown=msg.message
            )
        elif isinstance(msg, SendMessageChoicePrompt):
            query_id = chat_service.send_choice_reply_to_user_exchange(
                user_id=user.id,
                exchange_id=id,
                from_agent_id=msg.fromAgentId,
                prompt=msg.prompt,
                choices=msg.choices
            )
            return RepliedChoiceInfoResponse(
                queryId=query_id
            )
    except NonexistentExchangeError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

