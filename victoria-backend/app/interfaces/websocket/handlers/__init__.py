from app.interfaces.websocket.messages.subscription import Subscription
from app.interfaces.websocket.messages.event import EventContent, EventMessage
from app.services.event_bus import EventBusService, UnsubscribeHandle, Event
from app.containers import Container
from dependency_injector.wiring import inject, Provide
from typing import List, Optional, Callable
from asyncio import Queue, QueueFull, QueueShutDown, AbstractEventLoop
from pydantic import BaseModel
from abc import abstractmethod, ABC


class SubscriptionHandler(ABC):
    """Handler for a given kind of subscription.

    Args:
        send_queue (Queue[BaseModel]): The message queue where to send messages relevant to the subscription.
        event_loop (AbstractEventLoop): The event loop of the parent WebsocketConnection, where queue operations will be scheduled.
        event_bus_service (EventBusService): The event bus from which to take events.
    """

    @inject
    def __init__(
        self,
        send_queue: Queue[BaseModel],
        event_loop: AbstractEventLoop,
        event_bus_service: EventBusService = Provide[Container.event_bus],
    ):
        self._unsub_handles: List[UnsubscribeHandle] = []
        self._send_queue: Queue[BaseModel] = send_queue
        self._loop: AbstractEventLoop = event_loop
        self._bus: EventBusService = event_bus_service
        self._client_handler_ids: List[int] = []

    def disconnect_from_event_bus(self):
        """Disconnects this handler from the event bus."""
        for handle in self._unsub_handles:
            handle()

    def add_client_handler_id(self, handler_id: int, subscription: Subscription):
        """Adds the upstream client handler ID to the list of recipients.

        Args:
            handler_id (int): The handler ID to add.
            subscription (Subscription): The subscription details of the client.
        """
        if not self.can_handle_subscription(subscription):
            raise CannotHandleSubscriptionError()

        if handler_id not in self._client_handler_ids:
            self._client_handler_ids.append(handler_id)

    def remove_client_handler_id(self, handler_id: int):
        """Removes the upstream client handler ID from the list of recipients.

        Args:
            handler_id (int): The handler ID to remove.
        """
        if handler_id in self._client_handler_ids:
            self._client_handler_ids.remove(handler_id)

    @abstractmethod
    def can_handle_subscription(self, subscription: Subscription) -> bool:
        """Checks if the handler can also manage the given subscription.

        Args:
            subscription (Subscription): The subscription to check.

        Returns:
            True if the handler can handle the subscription, False otherwise.
        """
        raise NotImplementedError()

    def _subscribe_to_event_bus[T: Event](
        self, event: type[T], handler: Callable[[T], None]
    ):
        unsub_handle = self._bus.subscribe(event, handler)
        self._unsub_handles.append(unsub_handle)

    def _send_event(
        self, content: EventContent, handler_ids: Optional[List[int]] = None
    ):
        handlers = handler_ids or self._client_handler_ids
        if not handlers:
            return

        msg = EventMessage(handlerIds=handlers, content=content)

        def _send():
            try:
                self._send_queue.put_nowait(msg)
            except (QueueFull, QueueShutDown):
                # TODO: Add logging
                pass

        self._loop.call_soon_threadsafe(_send)


class CannotHandleSubscriptionError(Exception):
    def __init__(self):
        super().__init__("this handler cannot handle the given subscription")
