from app.services.auth import (
    AuthService,
    ExpiredLoginError,
    NotLoggedInError,
    AdminRequiredError,
)
from dependency_injector.wiring import Provide, inject
from app.containers import Container
from fastapi import Cookie, Depends, HTTPException, status
from typing import Annotated


@inject
async def get_non_admin_user(
    auth_service: Annotated[AuthService, Depends(Provide[Container.auth])],
    token: str = Cookie(None),
):
    try:
        return auth_service.get_as_non_admin_user(token)
    except ExpiredLoginError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Login has expired"
        )
    except NotLoggedInError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in"
        )


@inject
async def get_admin_user(
    auth_service: Annotated[AuthService, Depends(Provide[Container.auth])],
    token: str = Cookie(None),
):
    try:
        return auth_service.get_as_admin_user(token)
    except ExpiredLoginError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Login has expired"
        )
    except NotLoggedInError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in"
        )
    except AdminRequiredError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin priviliges required to access this resource",
        )
