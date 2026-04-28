from pydantic import BaseModel
from typing import Literal


class PingMessage(BaseModel):
    type: Literal["ping"] = "ping"


class PongMessage(BaseModel):
    type: Literal["pong"] = "pong"
