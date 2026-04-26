from . import SubscriptionHandler
from app.interfaces.websocket.messages.subscription import (
    Subscription,
    ExchangeMessagesSubscription,
)
from app.interfaces.rest_api.schema.messages import to_message_response
from app.interfaces.websocket.messages.events.exchange_agent_messages import (
    InitialAgentMessagesEvent,
    NewAgentMessageEvent,
)
from app.services.chat import (
    ChatService,
    ChatMessageSentEvent,
    NonexistentExchangeError,
    NonexistentMessageError,
)
from app.containers import Container
from dependency_injector.wiring import inject, Provide
from asyncio import Queue, AbstractEventLoop
from pydantic import BaseModel
from typing import override


class ExchangeAgentMessagesSubscriptionHandler(SubscriptionHandler):
    @inject
    def __init__(
        self,
        send_queue: Queue[BaseModel],
        event_loop: AbstractEventLoop,
        user_id: int,
        exchange_id: int,
        chat_service: ChatService = Provide[Container.chat],
    ):
        super().__init__(send_queue, event_loop)
        self._chat: ChatService = chat_service
        self._user_id: int = user_id
        self._exchange_id: int = exchange_id

        self._subscribe_to_event_bus(
            ChatMessageSentEvent, self._process_message_sent_event
        )

    @override
    def add_client_handler_id(self, handler_id: int, subscription: Subscription):
        super().add_client_handler_id(handler_id, subscription)

        if (
            isinstance(subscription, ExchangeMessagesSubscription)
            and subscription.sendInitial
        ):
            self._send_initial_messages(handler_id)

    @override
    def can_handle_subscription(self, subscription: Subscription) -> bool:
        return (
            isinstance(subscription, ExchangeMessagesSubscription)
            and subscription.exchangeId == self._exchange_id
        )

    def _process_message_sent_event(self, event: ChatMessageSentEvent):
        try:
            if (
                event.user_id == self._user_id
                and event.exchange_id == self._exchange_id
                and event.reply_id is not None
            ):
                message = self._chat.get_user_chat_message(
                    user_id=self._user_id, message_id=event.reply_id
                )
                message_response = to_message_response(message)
                reply = NewAgentMessageEvent(message=message_response)
                self._send_event(reply)
        except NonexistentMessageError:
            # TODO: Add logging
            pass

    def _send_initial_messages(self, handler_id: int):
        try:
            messages = self._chat.get_user_exchange_replies_after(
                user_id=self._user_id, exchange_id=self._exchange_id, after=0
            )
            message_responses = [to_message_response(x) for x in messages]
            event = InitialAgentMessagesEvent(messages=message_responses)
            self._send_event(event, [handler_id])
        except NonexistentExchangeError:
            # TODO: Add logging
            pass
