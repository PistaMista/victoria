import jwt
import time
from app.model.user import User
from app.config import settings

def create_auth_token_for_user(user: User, expires_in: int = 2592000) -> str:
    now = int(time.time())
    payload = {
        "user_id": user.id,
        "issued": now,
        "expires": now + expires_in
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token