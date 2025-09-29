from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal, Union, Any, List, Annotated
from app.services.chat import ChatOptionsDiff


class ChatResponse(BaseModel):
    id: int
    title: str
    summary: str

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

class ChatOptionsResponse(BaseModel):
    receiver: str
    enabledActionIds: List[int]


class ChatOptionsUpdate(BaseModel):
    receiver: Optional[str] = None
    enabledActionIds: Optional[List[int]] = None

    def to_diff(self) -> ChatOptionsDiff:
        return ChatOptionsDiff(
            receiver=self.receiver,
            enabled_action_ids=self.enabledActionIds
        )

class ChatDuplicate(BaseModel):
    toExchange: Optional[int] = None

class LLMUserMessage(BaseModel):
    role: Literal["user"] = "user"
    message: str

class LLMAssistantMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    agentName: str
    message: str

LLMMessage = Annotated[Union[LLMUserMessage, LLMAssistantMessage], Field(discriminator="role")]
