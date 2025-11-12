from pydantic import BaseModel
from app.model.monologue import Monologue
from app.model.thought import Thought
from app.model.invocation import Invocation
from typing import Literal, Optional, Dict, Any, List, Union

class MonologueListItemResponse(BaseModel):
    id: int
    agentId: int
    startTimestamp: int
    title: str
    summary: str
    status: Literal["RUNNING", "PENDING", "SUCCESS", "FAILURE"]

class MonologueResponse(BaseModel):
    id: int
    agentId: int
    startTimestamp: int
    endTimestamp: int
    title: str
    summary: str
    status: Literal["RUNNING", "PENDING", "SUCCESS", "FAILURE"]

class MonologueEnd(BaseModel):
    successful: bool
    reason: str

class TriggerInvocationParams(BaseModel):
    eventId: int

class TriggerInvocationResponse(BaseModel):
    type: Literal["TriggerInvocation"] = "TriggerInvocation"
    name: None = None
    parameters: TriggerInvocationParams

class ThoughtInvocationParams(BaseModel):
    thought: str

class ThoughtInvocationResponse(BaseModel):
    type: Literal["ThoughtInvocation"] = "ThoughtInvocation"
    name: None = None
    parameters: ThoughtInvocationParams

class ActionInvocationResponse(BaseModel):
    type: Literal["ActionInvocation"] = "ActionInvocation"
    name: str
    parameters: Dict[str, Any]

class SuccessInvocationParams(BaseModel):
    pass

class SuccessInvocationResponse(BaseModel):
    type: Literal["SuccessInvocation"] = "SuccessInvocation"
    name: None = None
    parameters: SuccessInvocationParams

class FailureInvocationParams(BaseModel):
    pass

class FailureInvocationResponse(BaseModel):
    type: Literal["FailureInvocation"] = "FailureInvocation"
    name: None = None
    parameters: FailureInvocationParams

InvocationResponse = Union[
    TriggerInvocationResponse,
    ThoughtInvocationResponse,
    ActionInvocationResponse,
    SuccessInvocationResponse,
    FailureInvocationResponse
]

class ThoughtResponse(BaseModel):
    id: int
    startTimestamp: int
    invocation: InvocationResponse
    result: str

def to_monologue_list_item_response(x: Monologue) -> MonologueListItemResponse:
    return MonologueListItemResponse(
        id=x.id,
        agentId=x.agent_id,
        startTimestamp=0,
        title=x.title,
        summary=x.summary,
        status=x.status.to_status_str()
    )

def to_monologue_response(x: Monologue) -> MonologueResponse:
    return MonologueResponse(
        id=x.id,
        agentId=x.agent_id,
        startTimestamp=int(x.dispatched_at.timestamp()),
        endTimestamp=int(x.modified_at.timestamp()),
        title=x.title,
        summary=x.summary,
        status=x.status.to_status_str()
    )

def to_invocation_response(x: Optional[Invocation], event_id: int) -> InvocationResponse:
    if x is None:
        return TriggerInvocationResponse(
            parameters=TriggerInvocationParams(
                eventId=event_id
            )
        )
    elif x.function_name == "think" and "content" in x.params:
        return ThoughtInvocationResponse(
            parameters=ThoughtInvocationParams(
                thought=x.params["content"]
            )
        )
    elif x.function_name == "end_monologue" and "successful" in x.params and x.params["successful"]:
        return SuccessInvocationResponse(
            parameters=SuccessInvocationParams()
        )
    elif x.function_name == "end_monologue" and "successful" in x.params and not x.params["successful"]:
        return FailureInvocationResponse(
            parameters=FailureInvocationParams()
        )
    else:
        return ActionInvocationResponse(
            name=x.function_name or "INVALID",
            parameters=x.params or {}
        )

def to_thought_response(x: Thought) -> ThoughtResponse:
    return ThoughtResponse(
        id=x.id,
        startTimestamp=int(x.timestamp.timestamp()),
        invocation=to_invocation_response(x.invocation, x.monologue.event_id),
        result=x.result or ""
    )
