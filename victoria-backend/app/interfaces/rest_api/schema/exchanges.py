from pydantic import BaseModel
from typing import Optional, List
from app.interfaces.rest_api.schema.messages import MessageResponse, to_message_response
from app.model.chat_exchange import ChatExchange


class ExchangeResponse(BaseModel):
    id: int
    chatId: int
    timestamp: int
    userMessage: Optional[MessageResponse]
    monologueIds: List[int]


def to_exchange_response(x: ChatExchange) -> ExchangeResponse:
    return ExchangeResponse(
        id=x.id,
        chatId=x.chat_id,
        timestamp=int(x.timestamp.timestamp()),
        userMessage=to_message_response(x.user_message)
        if x.user_message is not None
        else None,
        monologueIds=[
            monologue.id
            for event in x.triggered_chat_events
            for monologue in event.monologues
        ],
    )
