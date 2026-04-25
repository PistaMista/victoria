from . import SubscriptionHandler
from app.interfaces.websocket.messages.subscription import (
    Subscription,
    ChatExchangesSubscription,
)
from typing import override
from asyncio import Queue, AbstractEventLoop
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.services.chat import ChatService


class ChatExchangeSubscriptionHandler(SubscriptionHandler):
    @inject
    def __init__(
        self,
        send_queue: Queue[BaseModel],
        event_loop: AbstractEventLoop,
        user_id: int,
        chat_id: int,
        chat_service: ChatService = Provide[Container.chat],
    ):
        super().__init__(send_queue, event_loop)
        self._chat: ChatService = chat_service
        self._user_id: int = user_id
        self._chat_id: int = chat_id

    @override
    def can_handle_subscription(self, subscription: Subscription) -> bool:
        return (
            isinstance(subscription, ChatExchangesSubscription)
            and subscription.chatId == self._chat_id
        )
