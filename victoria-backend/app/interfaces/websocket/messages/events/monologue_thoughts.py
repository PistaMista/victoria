from pydantic import BaseModel
from app.interfaces.rest_api.schema.monologues import ThoughtResponse
from typing import Literal, List


class InitialThoughtEvent(BaseModel):
    type: Literal["initial"] = "initial"
    thoughts: List[ThoughtResponse]


class NewThoughtEvent(BaseModel):
    type: Literal["new"] = "new"
    thought: ThoughtResponse
