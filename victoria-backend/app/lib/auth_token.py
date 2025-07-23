import jwt
import time
from app.model.user import User
from app.config import settings
from typing import Optional

def create_auth_token_for_user(user: User, expires_in: int = 2592000) -> str:
    now = int(time.time())
    payload = {
        "user_id": user.id,
        "issued": now,
        "expires": now + expires_in
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token

def decode_token(token: str) -> Optional[dict]:
    try:
        token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return token
    except:
        return None