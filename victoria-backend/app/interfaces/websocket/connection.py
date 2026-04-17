from fastapi import WebSocket, WebSocketDisconnect, status
from .messages import Message
from .messages.heartbeat import PingMessage, PongMessage
from app.services.event_bus import EventBusService
from asyncio import Queue, TaskGroup, sleep, Task
from pydantic import BaseModel
from typing import Optional


class WebsocketConnection:
    def __init__(
        self,
        socket: WebSocket,
        event_bus_service: EventBusService,
        heartbeat_interval: float,
        heartbeat_timeout: float,
    ):
        self._socket: WebSocket = socket
        self._bus: EventBusService = event_bus_service
        self._heartbeat_interval: float = heartbeat_interval
        self._heartbeat_timeout: float = heartbeat_timeout

        self._send_queue: Queue[BaseModel] = Queue()
        self._missed_heartbeat: Optional[Task] = None

    async def start_managing(self):
        try:
            async with TaskGroup() as tg:
                tg.create_task(self._heartbeat_task(tg))
                tg.create_task(self._sender_task())
                tg.create_task(self._receive_task())
        except* WebSocketDisconnect:
            pass
        except* HeartbeatMissedError as e:
            await self._socket.close(status.WS_1011_INTERNAL_ERROR, reason=str(e))

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
            await self._send_queue.put(PingMessage())
            self._start_missed_heartbeat_task(tg)
            await sleep(self._heartbeat_interval)

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


class HeartbeatMissedError(Exception):
    def __init__(self):
        super().__init__("heartbeat ping not acknowledged")
