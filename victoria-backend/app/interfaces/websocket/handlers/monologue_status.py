from . import SubscriptionHandler
from app.interfaces.rest_api.schema.monologues import to_monologue_response
from app.interfaces.websocket.messages.subscription import (
    Subscription,
    MonologueStatusSubscription,
)
from app.interfaces.websocket.messages.events.monologue_status import (
    MonologueStatusEvent,
)
from app.services.monologues import (
    MonologueService,
    MonologueStatusChangedEvent,
    MonologueMetadataSetEvent,
    NonexistentMonologueError,
)
from app.containers import Container
from dependency_injector.wiring import inject, Provide
from asyncio import AbstractEventLoop, Queue
from pydantic import BaseModel
from typing import override, Optional


class MonologueStatusSubscriptionHandler(SubscriptionHandler):
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
            MonologueStatusChangedEvent, self._process_change_event
        )
        self._subscribe_to_event_bus(
            MonologueMetadataSetEvent, self._process_change_event
        )

    @override
    def add_client_handler_id(self, handler_id: int, subscription: Subscription):
        super().add_client_handler_id(handler_id, subscription)

        if (
            isinstance(subscription, MonologueStatusSubscription)
            and subscription.sendInitial
        ):
            self._send_status(handler_id)

    @override
    def can_handle_subscription(self, subscription: Subscription) -> bool:
        return (
            isinstance(subscription, MonologueStatusSubscription)
            and subscription.monologueId == self._monologue_id
        )

    def _process_change_event(
        self, event: MonologueStatusChangedEvent | MonologueMetadataSetEvent
    ):
        if event.user_id == self._user_id and event.monologue_id == self._monologue_id:
            self._send_status()

    def _send_status(self, handler_id: Optional[int] = None):
        try:
            monologue = self._monologue.get_user_monologue(
                user_id=self._user_id, monologue_id=self._monologue_id
            )
            monologue_msg = to_monologue_response(monologue)
            msg = MonologueStatusEvent(monologue=monologue_msg)

            if handler_id:
                self._send_event(msg, [handler_id])
            else:
                self._send_event(msg)
        except NonexistentMonologueError:
            # TODO: Add logging
            pass
