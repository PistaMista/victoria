from pydantic import BaseModel

class EventResponse(BaseModel):
    triggerId: int
    content: str

