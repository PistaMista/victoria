from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.db.session import get_db_session
from app.lib.user import get_current_user
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.model.user import User
from app.schema.user import UserLogin, UserRegister
from app.schema.error import Error
from app.lib.auth_token import create_auth_token_for_user
from bcrypt import checkpw, hashpw, gensalt

router = APIRouter()

@router.post("/login")
async def login(input: UserLogin, db: Session = Depends(get_db_session)) -> str:
    user = db.scalars(
            select(User).where(User.username == input.username)
        ).first()
    
    if not user is None:
        actual_pw = input.password.encode('utf-8')
        expected_hash = user.password_hash.encode('utf-8')

        if checkpw(actual_pw, expected_hash):
            token = create_auth_token_for_user(user)
            res = JSONResponse(
                status_code=200,
                content={}
            )
            res.set_cookie(
                key="token", 
                value=token,
                samesite="strict",
                httponly=True
            )
            return res

    raise HTTPException(status_code=401, detail="Invalid credentials")
    
        
    
@router.post("/register")
async def register(input: UserRegister, db: Session = Depends(get_db_session)):
    existing_user = db.scalars(
            select(User).where(User.username == input.username)
        ).first()
    
    if not existing_user is None:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
        
    new_user = User(
        username=input.username,
        password_hash=hashpw(input.password.encode('utf-8'), gensalt()).decode('utf-8')
    )
    db.add(new_user)
    db.flush()

    return JSONResponse(content={})

@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return JSONResponse(content={
        "username": user.username
    })