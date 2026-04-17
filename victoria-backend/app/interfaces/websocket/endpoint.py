from fastapi import APIRouter, Depends, WebSocket
from .connection import WebsocketConnection
from .dependencies.auth import get_non_admin_user
from dependency_injector.wiring import inject, Provide
from app.model.user import User
from app.containers import Container
from typing import Annotated, Callable

websocket_router = APIRouter()


@websocket_router.websocket("/ws")
@inject
async def websocket(
    ws: WebSocket,
    _: Annotated[User, Depends(get_non_admin_user)],
    connection_factory: Annotated[
        Callable[..., WebsocketConnection],
        Depends(Provide[Container.websocket_connection_factory.provider]),
    ],
):
    await ws.accept()
    connection = connection_factory(socket=ws)
    await connection.start_managing()
