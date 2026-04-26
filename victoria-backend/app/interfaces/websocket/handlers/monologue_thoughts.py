from . import SubscriptionHandler
from app.interfaces.websocket.messages.events.monologue_thoughts import (
    InitialThoughtEvent,
    NewThoughtEvent,
)
from app.interfaces.websocket.messages.subscription import (
    Subscription,
    MonologueThoughtsSubscription,
)
from app.interfaces.rest_api.schema.monologues import to_thought_response
from typing import override
from asyncio import Queue, AbstractEventLoop
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.services.monologues import (
    MonologueService,
    NonexistentMonologueError,
    MonologueThoughtAppendedEvent,
)


class MonologueThoughtsSubscriptionHandler(SubscriptionHandler):
    @inject
    def __init__(
        self,
        send_queue: Queue[BaseModel],
        event_loop: AbstractEventLoop,
        user_id: int,
        monologue_id: int,
        monologue_service: MonologueService = Provide[Container.monologue],
    ):
        super().__init__(send_queue, event_loop)
        self._monologue: MonologueService = monologue_service
        self._user_id: int = user_id
        self._monologue_id: int = monologue_id

        self._subscribe_to_event_bus(
            MonologueThoughtAppendedEvent, self._process_append_event
        )

    @override
    def add_client_handler_id(self, handler_id: int, subscription: Subscription):
        super().add_client_handler_id(handler_id, subscription)

        if (
            isinstance(subscription, MonologueThoughtsSubscription)
            and subscription.sendInitial
        ):
            self._send_initial_thoughts(handler_id)

    @override
    def can_handle_subscription(self, subscription: Subscription) -> bool:
        return (
            isinstance(subscription, MonologueThoughtsSubscription)
            and subscription.monologueId == self._monologue_id
        )

    def _process_append_event(self, event: MonologueThoughtAppendedEvent):
        if event.user_id == self._user_id and event.monologue_id == self._monologue_id:
            thought_msg = to_thought_response(event.thought)
            msg = NewThoughtEvent(thought=thought_msg)
            self._send_event(msg)

    def _send_initial_thoughts(self, handler_id: int):
        try:
            thoughts = self._monologue.get_user_monologue_thoughts(
                user_id=self._user_id, monologue_id=self._monologue_id
            )
            thought_msgs = [to_thought_response(x) for x in thoughts]
            msg = InitialThoughtEvent(thoughts=thought_msgs)
            self._send_event(msg, [handler_id])
        except NonexistentMonologueError:
            # TODO: Add logging
            pass
