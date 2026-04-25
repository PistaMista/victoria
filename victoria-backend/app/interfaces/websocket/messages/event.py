from pydantic import BaseModel
from typing import Union, List, Literal
from .events.monologue_thoughts import InitialThoughtEvent, NewThoughtEvent


EventContent = Union[InitialThoughtEvent, NewThoughtEvent]


class EventMessage(BaseModel):
    type: Literal["eventMessage"] = "eventMessage"
    handlerIds: List[int] = []
    content: EventContent
