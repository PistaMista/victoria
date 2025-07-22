from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.session import get_db_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.model.user import User
from app.schema.user import UserLogin, UserRegister
from app.schema.error import Error
from bcrypt import checkpw

router = APIRouter()

@router.post("/login")
async def login(input: UserLogin, db: Session = Depends(get_db_session)) -> str:
    err_msg = Error(error="Invalid credentials")
    user = db.scalars(
            select(User).where(User.username == input.username)
        ).first()
    
    if not user is None:
        actual_pw = input.password.encode('utf-8')
        expected_hash = user.password_hash.encode('utf-8')

        if checkpw(actual_pw, expected_hash):
            return JSONResponse(
                status_code=200,
                content=""            
            )

    return JSONResponse(
        status_code=401,
        content=err_msg.dict()
    )
    
        
    
@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db_session)):
    return []