from pydantic import BaseModel
from app.services.db import DatabaseService
from app.model.agent import Agent
from app.model.user import User
from app.model.language_model import LanguageModel
from app.model.monologue import Monologue, MonologueStatus
from app.model.trigger import Trigger
from app.model.action import Action
from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from copy import copy


class AgentService:
    def __init__(self, database_service: DatabaseService):
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
            agent = db.scalar(select(Agent).where(Agent.id == agent_id))

            if agent is None:
                raise NonexistentAgentError(agent_id)

            monologues_running = db.scalar(
                select(
                    exists().where(
                        Monologue.agent_id == agent_id,
                        Monologue.status == MonologueStatus.RUNNING,
                    )
                )
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
        enabled_action_ids: List[int],
    ):
        """Creates a new Agent for the given user."""
        with self._db.session() as db:
            owner = db.scalar(select(User).where(User.id == user_id))

            if owner is None:
                raise InvalidAgentSettingError(
                    f"Nonexistent user {user_id} can't be owner of this agent."
                )

            model = None
            if model_id is not None:
                model = db.scalar(
                    select(LanguageModel).where(
                        LanguageModel.id == model_id, LanguageModel.enabled
                    )
                )

                if model is None:
                    raise InvalidAgentSettingError(
                        f"Model with ID {model_id} is nonexistent or disabled."
                    )

            triggers = (
                db.scalars(
                    select(Trigger)
                    .join(Trigger.allowed_on_users)
                    .where(User.id == owner.id, Trigger.id.in_(enabled_trigger_ids))
                )
                .unique()
                .all()
            )

            if len(triggers) < len(enabled_trigger_ids):
                raise InvalidAgentSettingError(
                    "Cannot allow nonexistent or forbidden triggers for this agent."
                )

            actions = (
                db.scalars(
                    select(Action)
                    .join(Action.allowed_on_users)
                    .where(User.id == owner.id, Action.id.in_(enabled_action_ids))
                )
                .unique()
                .all()
            )

            if len(actions) < len(enabled_action_ids):
                raise InvalidAgentSettingError(
                    "Cannot allow nonexistent or forbidden actions for this agent."
                )

            new_agent = Agent(
                name=name,
                prompt=system_prompt,
                owner=owner,
                model=model,
                model_params=model_parameters,
                allowed_triggers=triggers,
                allowed_actions=actions,
            )

            db.add(new_agent)
            db.commit()

    def get_user_agent_by_id(self, user_id: int, agent_id: int) -> Agent:
        """Gets a given User's Agent by id."""
        with self._db.session() as db:
            agent = self._load_user_agent(db, user_id, agent_id)
            db.refresh(agent, attribute_names=["allowed_actions", "allowed_triggers"])
            return agent

    def update_user_agent(self, user_id: int, agent_id: int, diff: "AgentDiff"):
        """Updates a given User's Agent."""
        with self._db.session() as db:
            agent = self._load_user_agent(db, user_id, agent_id)

            if diff.name is not None:
                agent.name = diff.name

            if diff.model_id is not None:
                model = db.scalar(
                    select(LanguageModel).where(
                        LanguageModel.id == diff.model_id, LanguageModel.enabled
                    )
                )

                if model is None:
                    raise InvalidAgentSettingError(
                        "Cannot update Agent with nonexistent or disabled model."
                    )

                agent.model = model

            if diff.prompt is not None:
                agent.prompt = diff.prompt

            if diff.model_params is not None:
                # The copied dict is necessary for the ORM to detect changes
                changed = copy(agent.model_params)

                for key, value in diff.model_params.items():
                    if value is None:
                        changed.pop(key, None)
                    else:
                        changed[key] = value

                agent.model_params = changed

            if diff.enabled_trigger_ids is not None:
                triggers = (
                    db.scalars(
                        select(Trigger)
                        .join(Trigger.allowed_on_users)
                        .where(
                            User.id == agent.owner_id,
                            Trigger.id.in_(diff.enabled_trigger_ids),
                        )
                    )
                    .unique()
                    .all()
                )

                if len(triggers) < len(diff.enabled_trigger_ids):
                    raise InvalidAgentSettingError(
                        "Cannot allow nonexistent or forbidden triggers for this agent."
                    )

                agent.allowed_triggers = triggers

            if diff.enabled_action_ids is not None:
                actions = (
                    db.scalars(
                        select(Action)
                        .join(Action.allowed_on_users)
                        .where(
                            User.id == agent.owner_id,
                            Action.id.in_(diff.enabled_action_ids),
                        )
                    )
                    .unique()
                    .all()
                )

                if len(actions) < len(diff.enabled_action_ids):
                    raise InvalidAgentSettingError(
                        "Cannot allow nonexistent or forbidden actions for this agent."
                    )

                agent.allowed_actions = actions

            db.commit()

    def remove_user_agent(self, user_id: int, agent_id: int):
        """Deletes a given User's Agent."""
        with self._db.session() as db:
            agent = self._load_user_agent(db, user_id, agent_id)
            db.delete(agent)
            db.commit()

    def get_user_agent_monologues(self, user_id: int, agent_id: int) -> List[Monologue]:
        """Gets all running monologues of a given Agent."""
        with self._db.session() as db:
            agent = self._load_user_agent(db, user_id, agent_id)
            res = db.scalars(
                select(Monologue).where(
                    Monologue.agent_id == agent.id,
                    Monologue.status == MonologueStatus.RUNNING,
                )
            ).all()

            return res

    def _load_user_agent(self, db: Session, user_id: int, agent_id: int) -> Agent:
        agent = db.scalar(
            select(Agent)
            .where(Agent.id == agent_id, Agent.owner_id == user_id)
            .with_for_update()
        )

        if agent is None:
            raise NonexistentAgentError(agent_id)

        return agent


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
