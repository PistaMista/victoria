from pydantic import BaseModel
from app.services.db import DatabaseService
from app.model.agent import Agent
from app.model.monologue import Monologue
from typing import Optional, Dict, Any, List

class AgentService:
    def __init__(
        self,
        database_service: DatabaseService
    ):
        self._db: DatabaseService = database_service

    def get_user_agents(self, user_id: int) -> List[Agent]:
        """Gets all agents of the user with the given id."""
        pass

    def is_agent_running_monologues(self, agent_id: int) -> bool:
        """Finds out if the agent with the given id is currently running any monologues."""
        pass

    def add_user_agent(
        self,
        user_id: int,
        name: str,
        model_id: int,
        system_prompt: str,
        model_parameters: Dict[str, Any],
        enabled_trigger_ids: List[int],
        enabled_action_ids: List[int]
    ):
        """Creates a new Agent for the given user."""
        pass

    def get_user_agent_by_id(self, user_id: int, agent_id: int) -> Agent:
        """Gets a given User's Agent by id."""
        pass

    def update_user_agent(self, user_id: int, agent_id: int, diff: "AgentDiff"):
        """Updates a given User's Agent."""
        pass

    def remove_user_agent(self, user_id: int, agent_id: int):
        """Deletes a given User's Agent."""
        pass

    def get_user_agent_monologues(self, user_id: int, agent_id: int) -> List[Monologue]:
        """Gets all running monologues of a given Agent."""
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
