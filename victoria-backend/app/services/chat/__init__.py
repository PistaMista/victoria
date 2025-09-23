from pydantic import BaseModel
from typing import Optional, List

class ChatService:
    pass

class ChatOptionsDiff(BaseModel):
    receiver: Optional[str] = None
    enabled_action_ids: Optional[List[int]] = None

class NonexistentChatError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent chat with ID {id}")

class NonexistentExchangeError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent exchange with ID {id}")
