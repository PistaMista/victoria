from pydantic import BaseModel
from app.interfaces.rest_api.schema.messages import MessageResponse
from typing import Literal, List


class InitialAgentMessagesEvent(BaseModel):
    type: Literal["initial"] = "initial"
    messages: List[MessageResponse]


class NewAgentMessageEvent(BaseModel):
    type: Literal["new"] = "new"
    message: MessageResponse
