from app.services.auth import (
    AuthService,
    ExpiredLoginError,
    NotLoggedInError,
)
from dependency_injector.wiring import Provide, inject
from app.containers import Container
from fastapi import Cookie, Depends, WebSocketException, status
from typing import Annotated


@inject
async def get_non_admin_user(
    auth_service: Annotated[AuthService, Depends(Provide[Container.auth])],
    token: str = Cookie(None),
):
    try:
        return auth_service.get_as_non_admin_user(token)
    except ExpiredLoginError:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Login has expired"
        )
    except NotLoggedInError:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Not logged in"
        )
