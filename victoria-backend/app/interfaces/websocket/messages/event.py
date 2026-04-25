from pydantic import BaseModel
from typing import Union, List, Literal
from .events.monologue_thoughts import InitialThoughtEvent, NewThoughtEvent
from .events.chat_exchange import InitialExchangesEvent, NewExchangeEvent


EventContent = Union[
    InitialThoughtEvent, NewThoughtEvent, InitialExchangesEvent, NewExchangeEvent
]


class EventMessage(BaseModel):
    type: Literal["eventMessage"] = "eventMessage"
    handlerIds: List[int] = []
    content: EventContent
