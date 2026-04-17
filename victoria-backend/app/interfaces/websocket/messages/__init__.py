from .heartbeat import PingMessage, PongMessage
from typing import Union, Annotated
from pydantic import Field
from pydantic.type_adapter import TypeAdapter

Message = TypeAdapter(
    Annotated[Union[PingMessage, PongMessage], Field(discriminator="type")]
)
