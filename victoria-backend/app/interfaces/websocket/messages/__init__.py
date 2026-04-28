from .heartbeat import PingMessage, PongMessage
from .event import EventMessage
from .subscription import (
    SubscribeRequestMessage,
    SubscribeResponseMessage,
    UnsubscribeRequestMessage,
    UnsubscribeResponseMessage,
    SubscriptionCancelledMessage,
)
from typing import Union, Annotated
from pydantic import Field
from pydantic.type_adapter import TypeAdapter

Message = TypeAdapter(
    Annotated[
        Union[
            PingMessage,
            PongMessage,
            EventMessage,
            SubscribeRequestMessage,
            SubscribeResponseMessage,
            UnsubscribeRequestMessage,
            UnsubscribeResponseMessage,
            SubscriptionCancelledMessage,
        ],
        Field(discriminator="type"),
    ]
)
