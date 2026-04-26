from fastapi import WebSocket, WebSocketDisconnect, status
from .handlers import SubscriptionHandler
from .handlers.chat_exchange import ChatExchangeSubscriptionHandler
from .handlers.monologue_thoughts import MonologueThoughtsSubscriptionHandler
from .handlers.monologue_status import MonologueStatusSubscriptionHandler
from .messages import Message
from .messages.heartbeat import PingMessage, PongMessage
from .messages.subscription import (
    SubscribeRequestMessage,
    SubscribeResponseMessage,
    UnsubscribeRequestMessage,
    UnsubscribeResponseMessage,
    Subscription,
    ChatExchangesSubscription,
    MonologueThoughtsSubscription,
    MonologueStatusSubscription,
)
from app.services.event_bus import EventBusService
from app.model.user import User
from app.containers import Container
from asyncio import Queue, TaskGroup, sleep, Task, get_running_loop
from pydantic import BaseModel
from typing import Optional, Dict
from dependency_injector.wiring import inject, Provide


class WebsocketConnection:
    """Manager for a websocket connection, which converts and forwards events from a bus to the socket.

    Args:
        socket (WebSocket): The websocket connection to manage.
        user (User): The user initiating the connection.
        event_bus_service (EventBusService): The event bus to forward events from.
        heartbeat_interval (float): Interval between heartbeat messages to check if the client is healthy.
        heartbeat_timeout (float): Time to wait for a heartbeat response from client before closing the connection.
    """

    @inject
    def __init__(
        self,
        socket: WebSocket,
        user: User,
        event_bus_service: EventBusService = Provide[Container.event_bus],
        heartbeat_interval: float = Provide[Container.config.WS_HEARTBEAT_INTERVAL],
        heartbeat_timeout: float = Provide[Container.config.WS_HEARTBEAT_TIMEOUT],
    ):
        self._socket: WebSocket = socket
        self._user: User = user
        self._bus: EventBusService = event_bus_service
        self._heartbeat_interval: float = heartbeat_interval
        self._heartbeat_timeout: float = heartbeat_timeout

        self._send_queue: Queue[BaseModel] = Queue()
        self._missed_heartbeat: Optional[Task] = None

        self._subscription_handlers: Dict[int, SubscriptionHandler] = {}

    async def manage(self):
        """Starts managing the connection until it is closed."""
        try:
            async with TaskGroup() as tg:
                tg.create_task(self._heartbeat_task(tg))
                tg.create_task(self._sender_task())
                tg.create_task(self._receive_task())
        except* WebSocketDisconnect:
            pass
        except* HeartbeatMissedError as e:
            await self._socket.close(status.WS_1011_INTERNAL_ERROR, reason=str(e))
        finally:
            for handler in self._subscription_handlers.values():
                handler.disconnect_from_event_bus()
            self._subscription_handlers.clear()

    def _construct_subscription_handler(
        self, subscription: Subscription
    ) -> Optional[SubscriptionHandler]:
        loop = get_running_loop()
        match subscription:
            case ChatExchangesSubscription():
                return ChatExchangeSubscriptionHandler(
                    send_queue=self._send_queue,
                    event_loop=loop,
                    user_id=self._user.id,
                    chat_id=subscription.chatId,
                )
            case MonologueThoughtsSubscription():
                return MonologueThoughtsSubscriptionHandler(
                    send_queue=self._send_queue,
                    event_loop=loop,
                    user_id=self._user.id,
                    monologue_id=subscription.monologueId,
                )
            case MonologueStatusSubscription():
                return MonologueStatusSubscriptionHandler(
                    send_queue=self._send_queue,
                    event_loop=loop,
                    user_id=self._user.id,
                    monologue_id=subscription.monologueId,
                )

        return None

    async def _process_event_subscribe_request(self, msg: SubscribeRequestMessage):
        if msg.handlerId in self._subscription_handlers:
            reply = SubscribeResponseMessage(
                handlerId=msg.handlerId,
                success=False,
                reason=f"handler with id {msg.handlerId} is already subscribed",
            )
            await self._send_queue.put(reply)
            return

        for handler in self._subscription_handlers.values():
            if handler.can_handle_subscription(msg.subscription):
                handler.add_client_handler_id(msg.handlerId, msg.subscription)
                self._subscription_handlers[msg.handlerId] = handler
                break
        else:
            handler = self._construct_subscription_handler(msg.subscription)

            if handler is None or not handler.can_handle_subscription(msg.subscription):
                reply = SubscribeResponseMessage(
                    handlerId=msg.handlerId,
                    success=False,
                    reason="the server does not know how to handle this subscription",
                )
                await self._send_queue.put(reply)
                return

            handler.add_client_handler_id(msg.handlerId, msg.subscription)
            self._subscription_handlers[msg.handlerId] = handler

        reply = SubscribeResponseMessage(
            handlerId=msg.handlerId, success=True, reason=""
        )
        await self._send_queue.put(reply)

    async def _process_event_unsubscribe_request(self, msg: UnsubscribeRequestMessage):
        if msg.handlerId not in self._subscription_handlers:
            reply = UnsubscribeResponseMessage(
                handlerId=msg.handlerId,
                success=False,
                reason=f"handler with id {msg.handlerId} is not subscribed",
            )
            await self._send_queue.put(reply)
            return

        handler = self._subscription_handlers.pop(msg.handlerId)
        handler.remove_client_handler_id(msg.handlerId)

        if handler not in self._subscription_handlers.values():
            handler.disconnect_from_event_bus()

        reply = UnsubscribeResponseMessage(
            handlerId=msg.handlerId, success=True, reason=""
        )
        await self._send_queue.put(reply)

    def _start_missed_heartbeat_task(self, tg: TaskGroup):
        if self._missed_heartbeat is None:
            self._missed_heartbeat = tg.create_task(self._missed_heartbeat_task())

    def _stop_missed_heartbeat_task(self):
        if self._missed_heartbeat is not None:
            self._missed_heartbeat.cancel()
            self._missed_heartbeat = None

    async def _missed_heartbeat_task(self):
        await sleep(self._heartbeat_timeout)
        raise HeartbeatMissedError()

    async def _heartbeat_task(self, tg: TaskGroup):
        while True:
            await sleep(self._heartbeat_interval)
            await self._send_queue.put(PingMessage())
            self._start_missed_heartbeat_task(tg)

    async def _sender_task(self):
        while True:
            msg = await self._send_queue.get()
            await self._socket.send_json(msg.model_dump())

    async def _receive_task(self):
        while True:
            obj = await self._socket.receive_json()
            message = Message.validate_python(obj)

            match message:
                case PongMessage():
                    self._stop_missed_heartbeat_task()
                case SubscribeRequestMessage():
                    await self._process_event_subscribe_request(message)
                case UnsubscribeRequestMessage():
                    await self._process_event_unsubscribe_request(message)


class HeartbeatMissedError(Exception):
    def __init__(self):
        super().__init__("heartbeat ping not acknowledged")
