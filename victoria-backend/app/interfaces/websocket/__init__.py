from fastapi import APIRouter, Depends, WebSocket
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
