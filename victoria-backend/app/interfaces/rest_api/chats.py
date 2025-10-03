from fastapi import APIRouter, status, Depends, HTTPException, Request, Body
from dependency_injector.wiring import inject, Provide
from app.services.chat import ChatService, NonexistentChatError
from app.model.user import User
from app.model.chat_message import ChatMessageMarkdown
from app.containers import Container
from .schema.chats import ChatResponse, ChatOptionsResponse, ChatOptionsUpdate, ChatDuplicate, LLMMessage, LLMUserMessage, LLMAssistantMessage
from .schema.exchanges import ExchangeResponse, to_exchange_response
from .schema.messages import SendMessage, SendMessageChoicePrompt, SendMessageMarkdown, SentMarkdownInfoResponse, SentChoiceInfoResponse
from .dependencies.auth import get_non_admin_user
from typing import List, Annotated, Union
import time

router = APIRouter()

@router.get("/", response_model=List[ChatResponse])
@inject
async def list_chats(
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> List[ChatResponse]:
    chats = chat_service.get_user_chats(
        user_id=user.id
    )
    return [ChatResponse.model_validate(x) for x in chats]

@router.post("/", response_model=ChatResponse)
@inject
async def create_chat(
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> ChatResponse:
    created_chat_id = chat_service.create_user_chat(
        user_id=user.id
    )
    created_chat = chat_service.get_user_chat(
        user_id=user.id,
        chat_id=created_chat_id
    )
    return ChatResponse.model_validate(created_chat)

@router.get("/receivers", response_model=List[str])
@inject
async def list_receivers(
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> List[str]:
    return chat_service.get_user_chat_receivers(
        user_id=user.id
    )

@router.get("/{id}", response_model=ChatResponse)
@inject
async def get_chat_info(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> ChatResponse:
    try:
        chat = chat_service.get_user_chat(
            user_id=user.id,
            chat_id=id
        )
        return ChatResponse.model_validate(chat)
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@router.delete("/{id}")
@inject
async def delete_chat(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> None:
    try:
        chat_service.remove_user_chat(
            user_id=user.id,
            chat_id=id
        )
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.post("/{id}/duplicate", response_model=int)
@inject
async def duplicate_chat(
    id: int,
    body: ChatDuplicate,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> int:
    try:
        new_chat_id = chat_service.duplicate_user_chat(
            user_id=user.id,
            chat_id=id,
            last_exchange_id=body.toExchange
        )
        return new_chat_id
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.post("/{id}/send-message", response_model=Union[SentChoiceInfoResponse, SentMarkdownInfoResponse])
@inject
async def send_message_to_chat(
    id: int,
    msg: SendMessage,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> Union[SentChoiceInfoResponse, SentMarkdownInfoResponse]:
    try:
        if isinstance(msg, SendMessageMarkdown):
            exchange_id = chat_service.send_markdown_message_to_user_chat(
                user_id=user.id,
                chat_id=id,
                from_agent_id=msg.fromAgentId,
                markdown=msg.message
            )
            return SentMarkdownInfoResponse(
                exchangeId=exchange_id
            )
        elif isinstance(msg, SendMessageChoicePrompt):
            exchange_id, query_id = chat_service.send_choice_message_to_user_chat(
                user_id=user.id,
                chat_id=id,
                from_agent_id=msg.fromAgentId,
                prompt=msg.prompt,
                choices=msg.choices
            )
            return SentChoiceInfoResponse(
                exchangeId=exchange_id,
                queryId=query_id
            )
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.get("/{id}/exchanges", response_model=List[ExchangeResponse])
@inject
async def get_exchanges_long_poll(
    id: int,
    after: int,
    request: Request,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> List[ExchangeResponse]:
    try:
        while not await request.is_disconnected():
            new = chat_service.get_user_chat_exchanges_after(
                user_id=user.id,
                chat_id=id,
                after=after
            )

            if new:
                return [to_exchange_response(x) for x in new]

            time.sleep(1.0)

        return []
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.get("/{id}/options", response_model=ChatOptionsResponse)
@inject
async def get_chat_options(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> ChatOptionsResponse:
    try:
        chat = chat_service.get_user_chat(
            user_id=user.id,
            chat_id=id
        )
        return ChatOptionsResponse(
            receiver=chat.receiver,
            enabledActionIds=[x.id for x in chat.allowed_actions]
        )
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.put("/{id}/options")
@inject
async def set_chat_options(
    id: int,
    body: ChatOptionsUpdate,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])]
) -> None:
    try:
        chat_service.update_user_chat_options(
            user_id=user.id,
            chat_id=id,
            options=body.to_diff()
        )
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.post("/{id}/summary")
@inject
async def set_chat_summary(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])],
    body: str = Body(..., media_type="application/json")
) -> None:
    try:
        chat_service.set_user_chat_summary(
            user_id=user.id,
            chat_id=id,
            summary=body
        )
    except NonexistentChatError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.get("/{id}/history", response_model=List[LLMMessage])
@inject
async def get_chat_history(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    chat_service: Annotated[ChatService, Depends(Provide[Container.chat])],
) -> List[LLMMessage]:
    try:
        msgs = chat_service.get_user_chat_messages(
            user_id=user.id,
            chat_id=id
        )

        result = []
        for msg in msgs:
            # TODO: Choice prompt messages are ignored for now. How should they be handled?
            if isinstance(msg, ChatMessageMarkdown):
                if msg.sending_user is not None:
                    result.append(LLMUserMessage(
                        message=msg.markdown
                    ))
                elif msg.sending_agent is not None:
                    result.append(LLMAssistantMessage(
                        agentName=msg.sending_agent.name,
                        message=msg.markdown
                    ))

        return result
    except NonexistentChatError as err: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

