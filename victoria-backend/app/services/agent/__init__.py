from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class AgentService:
    pass

class AgentDiff(BaseModel):
    name: Optional[str] = None
    model_id: Optional[int] = None
    prompt: Optional[str] = None
    model_params: Optional[Dict[str, Any]] = None
    enabled_trigger_ids: Optional[List[int]] = None
    enabled_action_ids: Optional[List[int]] = None

class InvalidAgentSettingError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"tried to set an invalid value for property of agent: {msg}")

class NonexistentAgentError(Exception):
    def __init__(self, id: int):
        super().__init__(f"agent with ID {id} does not exist")
