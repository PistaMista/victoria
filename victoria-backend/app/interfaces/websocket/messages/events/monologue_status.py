from pydantic import BaseModel
from app.interfaces.rest_api.schema.monologues import MonologueResponse


class MonologueStatusEvent(BaseModel):
    monologue: MonologueResponse
