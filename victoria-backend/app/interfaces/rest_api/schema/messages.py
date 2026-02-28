from pydantic import BaseModel, Field
from app.model.chat_message import (
    ChatMessage,
    ChatMessageMarkdown,
    ChatMessageChoicePrompt,
)
from typing import Literal, Union, Any, List, Annotated, Optional


class PromptChoice(BaseModel):
    value: Any


class MarkdownContent(BaseModel):
    type: Literal["markdown"] = "markdown"
    markdownText: str


class ChoicePromptContent(BaseModel):
    type: Literal["choice_prompt"] = "choice_prompt"
    queryId: int
    prompt: str
    choices: List[PromptChoice]


class MessageResponse(BaseModel):
    id: int
    timestamp: int
    senderName: str
    content: Annotated[
        Union[MarkdownContent, ChoicePromptContent], Field(discriminator="type")
    ]


def to_message_response(x: ChatMessage) -> MessageResponse:
    content = None
    if isinstance(x, ChatMessageMarkdown):
        content = MarkdownContent(markdownText=x.markdown)
    elif isinstance(x, ChatMessageChoicePrompt):
        content = ChoicePromptContent(
            queryId=x.id,
            prompt=x.prompt,
            choices=[PromptChoice(value=x.value) for x in x.choices],
        )

    if content is None:
        content = MarkdownContent(markdownText="INVALID CONTENT TYPE, PLEASE FIX")

    return MessageResponse(
        id=x.id,
        timestamp=int(x.timestamp.timestamp()),
        senderName=x.sending_user.username
        if x.sending_user
        else x.sending_agent.name
        if x.sending_agent
        else "Unknown",
        content=content,
    )


class SendMessageMarkdown(BaseModel):
    type: Literal["markdown"]
    message: str
    fromAgentId: Optional[int] = None


class SendMessageChoicePrompt(BaseModel):
    type: Literal["choice_prompt"]
    prompt: str
    choices: List[Any]
    fromAgentId: Optional[int] = None


SendMessage = Annotated[
    Union[SendMessageMarkdown, SendMessageChoicePrompt], Field(discriminator="type")
]


class SentMarkdownInfoResponse(BaseModel):
    exchangeId: int


class SentChoiceInfoResponse(BaseModel):
    exchangeId: int
    queryId: int


class RepliedChoiceInfoResponse(BaseModel):
    queryId: int
