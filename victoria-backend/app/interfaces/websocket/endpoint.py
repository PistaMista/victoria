from fastapi import APIRouter, Depends, WebSocket
from .connection import WebsocketConnection
from .dependencies.auth import get_non_admin_user
from app.model.user import User
from typing import Annotated

websocket_router = APIRouter()


@websocket_router.websocket("/ws")
async def websocket(
    ws: WebSocket,
    user: Annotated[User, Depends(get_non_admin_user)],
):
    await ws.accept()
    connection = WebsocketConnection(socket=ws, user=user)
    await connection.manage()
