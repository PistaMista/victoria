from . import SubscriptionHandler
from app.interfaces.websocket.messages.subscription import (
    Subscription,
    ChatExchangesSubscription,
)
from app.interfaces.websocket.messages.events.chat_exchange import (
    InitialExchangesEvent,
    NewExchangeEvent,
)
from app.interfaces.rest_api.schema.exchanges import to_exchange_response
from typing import override
from asyncio import Queue, AbstractEventLoop
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.services.chat import (
    ChatService,
    ChatExchangeCreatedEvent,
    NonexistentChatError,
    NonexistentExchangeError,
)


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

        self._subscribe_to_event_bus(
            ChatExchangeCreatedEvent, self._process_exchange_create_event
        )

    @override
    def add_client_handler_id(self, handler_id: int, subscription: Subscription):
        super().add_client_handler_id(handler_id, subscription)

        if (
            isinstance(subscription, ChatExchangesSubscription)
            and subscription.sendInitial
        ):
            self._send_initial_exchanges(handler_id)

    @override
    def can_handle_subscription(self, subscription: Subscription) -> bool:
        return (
            isinstance(subscription, ChatExchangesSubscription)
            and subscription.chatId == self._chat_id
        )

    def _process_exchange_create_event(self, event: ChatExchangeCreatedEvent):
        try:
            if event.user_id == self._user_id and event.chat_id == self._chat_id:
                exchange = self._chat.get_user_chat_exchange(
                    self._user_id, event.exchange_id
                )
                msg = NewExchangeEvent(exchange=to_exchange_response(exchange))
                self._send_event(msg)
        except NonexistentExchangeError:
            # TODO: Add logging
            pass

    def _send_initial_exchanges(self, handler_id: int):
        try:
            exchanges = self._chat.get_user_chat_exchanges_after(
                self._user_id, self._chat_id, 0
            )
            exchange_msgs = [to_exchange_response(x) for x in exchanges]
            msg = InitialExchangesEvent(exchanges=exchange_msgs)
            self._send_event(msg, [handler_id])
        except NonexistentChatError:
            # TODO: Add logging
            pass
