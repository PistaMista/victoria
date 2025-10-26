from app.services.user import UserService, NonexistentUserError
from app.model.user import User, Role
import jwt
from typing import Optional
import time
from bcrypt import checkpw

class AuthService:
    def __init__(
            self, 
            user_service: UserService, 
            jwt_secret: str, 
            login_lifetime: int
    ):
        self._user: UserService = user_service
        self._jwt_secret: str = jwt_secret
        self._login_lifetime: int = login_lifetime
    
    def get_login_token(self, username: str, password: str) -> str:
        user = self._user.get_user_by_name(username)

        if user is not None:
            actual_pw = password.encode('utf-8')
            expected_hash = user.password_hash.encode('utf-8')
            
            if checkpw(actual_pw, expected_hash):
                now = int(time.time())
                payload = {
                    "user_id": user.id,
                    "issued": now,
                    "expires": now + self._login_lifetime
                }
                
                return jwt.encode(payload, self._jwt_secret, algorithm="HS256")

        raise InvalidLoginError()
    
    def _get_as_any_user(self, token: Optional[str]) -> User:
        if token is None:
            raise NotLoggedInError()

        now = int(time.time())

        try:
            jwt_token = jwt.decode(token, self._jwt_secret, algorithms=["HS256"])

            if not isinstance(jwt_token, dict):
                raise InvalidLoginError()

            user_id = jwt_token.get("user_id", None)
            expiry = jwt_token.get("expires", None)

            if not isinstance(user_id, int) or not isinstance(expiry, int):
                raise InvalidLoginError()

            if now > expiry:
                raise ExpiredLoginError()

            try:
                user = self._user.get_user_by_id(user_id)
                return user
            except NonexistentUserError:
                raise ExpiredLoginError()
            
        except jwt.DecodeError as e:
            # If the given token is not a JWT token, it is a Monologue agent_token
            agent_token = token.encode("utf-8")

            try:
                user = self._user.get_user_by_running_monologue_agent_token(agent_token)
                # Downgrade the returned user role to USER, agents never have admin privileges
                user.role = Role.USER
                return user
            except NonexistentUserError:
                raise InvalidLoginError()
        except Exception as e:
            raise e
    
    def get_as_non_admin_user(self, token: str) -> User:
        return self._get_as_any_user(token)
    
    def get_as_admin_user(self, token: str) -> User:
        user = self._get_as_any_user(token)

        if user.role != Role.ADMIN:
            raise AdminRequiredError()
        
        return user
            

class InvalidLoginError(Exception):
    def __init__(self):
        super().__init__("invalid login credentials")

class ExpiredLoginError(Exception):
    def __init__(self):
        super().__init__("expired login")

class NotLoggedInError(Exception):
    def __init__(self):
        super().__init__("not logged in")

class AdminRequiredError(Exception):
    def __init__(self):
        super().__init__("admin privileges required")
