from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.model.user import Role
from app.interfaces.rest_api.schema.user import UserLogin, UserRegister
from app.services.auth import AuthService, InvalidLoginError
from app.services.user import User, UserService, UserExistsError
from app.containers import Container
from dependency_injector.wiring import Provide, inject
from .dependencies.auth import get_non_admin_user, get_admin_user

router = APIRouter()

@router.post("/login")
@inject
async def login(
    input: UserLogin, 
    auth_service: Annotated[AuthService, Depends(Provide[Container.auth])]
):
    try:
        token = auth_service.get_login_token(input.username, input.password)
        res = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={}
        )
        res.set_cookie(
            key="token", 
            value=token,
            samesite="strict",
            httponly=True
        )
        return res
    except InvalidLoginError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

@router.post("/register")
@inject
async def register(
    input: UserRegister,
    user_service: Annotated[UserService, Depends(Provide[Container.user])]
):
    try:
        is_first_user = not user_service.is_any_user_registered()
        user_service.create_user(
            username=input.username, 
            password=input.password,
            role=Role.ADMIN if is_first_user else Role.USER
        )
        
        return JSONResponse(content={})
    except UserExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

@router.get("/me")
async def me(
    user: Annotated[User, Depends(get_non_admin_user)]
):
    return JSONResponse(content={
        "username": user.username,
        "role": str(user.role)
    })

@router.get("/me/admin")
async def me_admin(
    user: Annotated[User, Depends(get_admin_user)]
):
    return JSONResponse(content={
        "username": user.username,
        "role": str(user.role)
    })
