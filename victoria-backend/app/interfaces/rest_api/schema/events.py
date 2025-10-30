from pydantic import BaseModel
from typing import Optional

class EventResponse(BaseModel):
    triggerId: Optional[int]
    content: str

