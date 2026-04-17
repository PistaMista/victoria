from typing import Callable, Dict, List, Any

UnsubscribeHandle = Callable[[], None]


class EventBusService:
    def __init__(self):
        self._event_handlers: Dict[Any, List[Callable]] = {}

    def publish(self, event: "Event"):
        """Publishes an event to the bus."""
        handlers = self._event_handlers.get(type(event), [])

        for handler in handlers:
            handler(event)

    def subscribe[T: Event](
        self, event: type[T], handler: Callable[[T], None]
    ) -> UnsubscribeHandle:
        """Subscribes to an event on the bus.

        Returns:
            A handle to unsubscribe from the event.
        """
        handlers = self._event_handlers.setdefault(event, [])
        handlers.append(handler)

        def unsubscribe_handle():
            if handler in handlers:
                handlers.remove(handler)

        return unsubscribe_handle


class Event:
    pass
