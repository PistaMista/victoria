from pydantic import BaseModel
from typing import Literal, Optional, Dict, Any, List

class MonologueListItemResponse(BaseModel):
    id: int
    agentId: int
    startTimestamp: int
    title: str
    summary: str
    status: Literal["RUNNING", "PENDING", "SUCCESS", "FAILURE"]

