from pydantic import BaseModel
from app.services.agent import AgentDiff
from typing import Literal, Optional, Dict, Any, List


class AgentListItemResponse(BaseModel):
    id: int
    name: str
    status: Literal["BUSY"] | Literal["IDLE"]


class AgentResponse(BaseModel):
    id: int
    name: str
    thumbnailDataURI: None = None
    status: Literal["BUSY"] | Literal["IDLE"]
    baseModelId: int
    systemPrompt: str
    modelParameters: Dict[str, Any]
    enabledTriggers: List[int]
    enabledActions: List[int]


class AgentCreate(BaseModel):
    id: Optional[int] = None
    name: str
    baseModelId: int
    systemPrompt: str
    modelParameters: Dict[str, Any]
    enabledTriggers: List[int]
    enabledActions: List[int]


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    baseModelId: Optional[int] = None
    systemPrompt: Optional[str] = None
    modelParameters: Optional[Dict[str, Any]] = None
    enabledTriggers: Optional[List[int]] = None
    enabledActions: Optional[List[int]] = None

    def to_diff(self) -> AgentDiff:
        return AgentDiff(
            name=self.name,
            model_id=self.baseModelId,
            prompt=self.systemPrompt,
            model_params=self.modelParameters,
            enabled_trigger_ids=self.enabledTriggers,
            enabled_action_ids=self.enabledActions,
        )
