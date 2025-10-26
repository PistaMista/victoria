from pydantic import BaseModel
from app.services.db import DatabaseService
from app.model.agent import Agent
from app.model.user import User
from app.model.language_model import LanguageModel
from app.model.monologue import Monologue, MonologueStatus
from app.model.trigger import Trigger
from app.model.action import Action
from sqlalchemy import select, exists
from typing import Optional, Dict, Any, List

class AgentService:
    def __init__(
        self,
        database_service: DatabaseService
    ):
        self._db: DatabaseService = database_service

    def get_user_agents(self, user_id: int) -> List[Agent]:
        """Gets all agents of the user with the given id."""
        with self._db.session() as db:
            res = db.scalars(
                select(Agent).join(Agent.owner).where(User.id == user_id)
            ).all()

            return res

    def is_agent_running_monologues(self, agent_id: int) -> bool:
        """Finds out if the agent with the given id is currently running any monologues."""
        with self._db.session() as db:
            agent = db.scalar(
                select(Agent).where(Agent.id == agent_id)
            )

            if agent is None:
                raise NonexistentAgentError(agent_id)

            monologues_running = db.scalar(
                select(exists()
                       .where(
                           Monologue.agent_id == agent_id,
                           Monologue.status == MonologueStatus.RUNNING
                        ))
            )

            return monologues_running

    def add_user_agent(
        self,
        user_id: int,
        name: str,
        model_id: Optional[int],
        system_prompt: str,
        model_parameters: Dict[str, Any],
        enabled_trigger_ids: List[int],
        enabled_action_ids: List[int]
    ):
        """Creates a new Agent for the given user."""
        with self._db.session() as db:
            owner = db.scalar(
                select(User).where(User.id == user_id)
            )

            if owner is None:
                raise InvalidAgentSettingError(f"Nonexistent user {user_id} can't be owner of this agent.")

            model = None
            if model_id is not None:
                model = db.scalar(
                    select(LanguageModel).where(LanguageModel.id == model_id)
                )

                if model is None or not model.enabled:
                    raise InvalidAgentSettingError(f"Model with ID {model_id} is nonexistent or disabled.")

            triggers = db.scalars(
                select(Trigger)
                .join(Trigger.allowed_on_users)
                .where(
                    User.id == owner.id,
                    Trigger.id.in_(enabled_trigger_ids)
                )
            ).unique().all()

            if len(triggers) < len(enabled_trigger_ids):
                raise InvalidAgentSettingError("Cannot allow nonexistent or forbidden triggers for this agent.")

            actions = db.scalars(
                select(Action)
                .join(Action.allowed_on_users)
                .where(
                    User.id == owner.id,
                    Action.id.in_(enabled_action_ids)
                )
            ).unique().all()

            if len(actions) < len(enabled_action_ids):
                raise InvalidAgentSettingError("Cannot allow nonexistent or forbidden actions for this agent.")

            new_agent = Agent(
                name=name,
                prompt=system_prompt,
                owner=owner,
                model=model,
                model_params=model_parameters,
                allowed_triggers=triggers,
                allowed_actions=actions
            )

            db.add(new_agent)
            db.commit()


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
