from pydantic import BaseModel
from typing import Union, List, Literal
from .events.monologue_thoughts import InitialThoughtEvent, NewThoughtEvent
from .events.monologue_status import MonologueStatusEvent
from .events.chat_exchange import InitialExchangesEvent, NewExchangeEvent
from .events.exchange_agent_messages import (
    InitialAgentMessagesEvent,
    NewAgentMessageEvent,
)


EventContent = Union[
    InitialThoughtEvent,
    NewThoughtEvent,
    InitialExchangesEvent,
    NewExchangeEvent,
    MonologueStatusEvent,
    InitialAgentMessagesEvent,
    NewAgentMessageEvent,
]


class EventMessage(BaseModel):
    type: Literal["eventMessage"] = "eventMessage"
    handlerIds: List[int] = []
    content: EventContent
