from pydantic import BaseModel, Field
from typing import Literal, Union, Annotated


class ChatExchangesSubscription(BaseModel):
    type: Literal["chat_exchanges"] = "chat_exchanges"
    sendInitial: bool = True
    chatId: int


class ExchangeMessagesSubscription(BaseModel):
    type: Literal["exchange_agent_messages"] = "exchange_agent_messages"
    sendInitial: bool = True
    exchangeId: int


class MonologueStatusSubscription(BaseModel):
    type: Literal["monologue_status"] = "monologue_status"
    sendInitial: bool = True
    monologueId: int


class MonologueThoughtsSubscription(BaseModel):
    type: Literal["monologue_thoughts"] = "monologue_thoughts"
    sendInitial: bool = True
    monologueId: int


Subscription = Annotated[
    Union[
        ChatExchangesSubscription,
        ExchangeMessagesSubscription,
        MonologueStatusSubscription,
        MonologueThoughtsSubscription,
    ],
    Field(discriminator="type"),
]


class SubscribeRequestMessage(BaseModel):
    type: Literal["subscribeRequest"] = "subscribeRequest"
    handlerId: int
    subscription: Subscription


class SubscribeResponseMessage(BaseModel):
    type: Literal["subscribeResponse"] = "subscribeResponse"
    handlerId: int
    success: bool
    reason: str


class UnsubscribeRequestMessage(BaseModel):
    type: Literal["unsubscribeRequest"] = "unsubscribeRequest"
    handlerId: int


class UnsubscribeResponseMessage(BaseModel):
    type: Literal["unsubscribeResponse"] = "unsubscribeResponse"
    handlerId: int
    success: bool
    reason: str


class SubscriptionCancelledMessage(BaseModel):
    type: Literal["subscriptionCancelled"] = "subscriptionCancelled"
    handlerId: int
