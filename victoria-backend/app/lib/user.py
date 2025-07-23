from fastapi import HTTPException, Cookie, Depends
from app.lib.auth_token import decode_token
from app.model.user import User
from app.db.session import get_db_session
from sqlalchemy import select
from sqlalchemy.orm import Session
import time


def get_current_user(token: str = Cookie(None), session: Session = Depends(get_db_session)):
    now = time.time()
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Not logged in"
        )
    
    decoded = decode_token(token)

    if decoded is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid authentication token"
        )
    
    if now > decoded["expires"]:
        raise HTTPException(
            status_code=401,
            detail="Login expired, please log in again"
        )
    
    user = session.scalars(
        select(User).where(User.id == decoded["user_id"])        
    ).first()
    
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User no longer exists"
        )
    
    return user
