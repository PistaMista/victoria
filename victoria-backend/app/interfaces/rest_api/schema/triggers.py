from pydantic import BaseModel, field_validator, ConfigDict
from typing import Literal, Union, Optional
from app.model.trigger import Trigger, TimerTrigger, PollTrigger, ChatTrigger, WebhookTrigger


class TimerSettings(BaseModel):
    type: Literal["timer"] = "timer"
    interval: int

class PollSettings(BaseModel):
    type: Literal["poll"] = "poll"
    interval: int
    url: str

class ChatSettings(BaseModel):
    type: Literal["chat"] = "chat"
    receiver: str

class WebhookSettings(BaseModel):
    type: Literal["webhook"] = "webhook"
    url: str

TriggerSettings = Union[
    TimerSettings, 
    PollSettings, 
    ChatSettings, 
    WebhookSettings
]

class TriggerCreate(BaseModel):
    name: str
    template: str
    parser: Literal["identity"]
    settings: TriggerSettings

class TriggerListItemResponse(BaseModel):
    id: int
    name: str
    type: Literal["timer", "poll", "chat", "webhook"]

    @field_validator('type', mode='before')
    @classmethod
    def lowercase_type(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

class TriggerResponse(BaseModel):
    id: int
    name: str
    template: str
    parser: Literal["identity"]
    settings: TriggerSettings

class TimerSettingsUpdate(BaseModel):
    type: Optional[Literal["timer"]] = None
    interval: Optional[int] = None

class PollSettingsUpdate(BaseModel):
    type: Optional[Literal["poll"]] = None
    interval: Optional[int] = None
    url: Optional[str] = None

class ChatSettingsUpdate(BaseModel):
    type: Optional[Literal["chat"]] = None
    receiver: Optional[str] = None

class WebhookSettingsUpdate(BaseModel):
    type: Optional[Literal["webhook"]] = None
    url: Optional[str] = None

TriggerSettingsUpdate = Union[
    TimerSettingsUpdate,
    PollSettingsUpdate,
    ChatSettingsUpdate,
    WebhookSettingsUpdate
]

class TriggerUpdate(BaseModel):
    name: Optional[str] = None
    template: Optional[str] = None
    settings: Optional[TriggerSettingsUpdate] = None

def to_trigger_response(x: Trigger) -> TriggerResponse:
    settings = TimerSettings(interval=0)

    if isinstance(x, TimerTrigger):
        settings = TimerSettings(
            interval=x.interval
        )
    elif isinstance(x, PollTrigger):
        settings = PollSettings(
            interval=x.interval,
            url=x.url
        )
    elif isinstance(x, ChatTrigger):
        settings = ChatSettings(
            receiver=x.receiver
        )
    elif isinstance(x, WebhookTrigger):
        settings = WebhookSettings(
            url=x.endpoint
        )

    return TriggerResponse(
        id=x.id,
        name=x.name,
        template=x.template,
        parser="identity",
        settings=settings
    )


