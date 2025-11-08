from app.services.db import DatabaseService
from app.services.action import ActionService
from app.services.llm import UserMessage, AssistantMessage
from app.model.agent import Agent
from app.model.monologue import Monologue, MonologueStatus
from app.model.thought import Thought
from app.model.invocation import Invocation
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, case, or_
from sqlalchemy.orm import joinedload, Session
from datetime import datetime, UTC
from copy import copy
import json

class MonologueService:
    def __init__(
        self,
        database_service: DatabaseService,
        action_service: ActionService
    ):
        self._db: DatabaseService = database_service
        self._action: ActionService = action_service

    def get_user_monologues(self, user_id: int, status_filter: Optional[MonologueStatus] = None, search_query: Optional[str] = None) -> List[Monologue]:
        """Gets all of the given User's monologues."""
        with self._db.session() as db:
            stmt = select(Monologue).join(Monologue.agent).where(Agent.owner_id == user_id)

            if status_filter is not None:
                stmt = stmt.where(Monologue.status == status_filter)

            if search_query is not None:
                stmt = stmt.where(or_(
                    func.lower(Monologue.title).like(f"%{search_query.lower()}%"),
                    func.lower(Monologue.summary).like(f"%{search_query.lower()}%")
                ))

            status_order = case(
                {
                    MonologueStatus.RUNNING.name: 1,
                    MonologueStatus.PENDING.name: 2,
                    MonologueStatus.SUCCESS.name: 3,
                    MonologueStatus.FAILURE.name: 3
                },
                value=Monologue.status
            )

            stmt = stmt.order_by(status_order.asc(), Monologue.modified_at.desc())

            res = db.scalars(stmt).all()
            return res

    def get_user_monologue(self, user_id: int, monologue_id: int) -> Monologue:
        """Gets the given Monologue."""
        with self._db.session() as db:
            res = self._load_user_monologue(db, user_id, monologue_id)
            return res

    def end_user_monologue(self, user_id: int, monologue_id: int, successful: bool):
        """Ends the given Monologue with either SUCCESS or FAILURE."""
        with self._db.session() as db:
            monologue = self._load_user_monologue(db, user_id, monologue_id)
            self.set_monologue_status(
                id=monologue.id, 
                status=MonologueStatus.SUCCESS if successful else MonologueStatus.FAILURE
            )

    def get_user_monologue_thoughts(self, user_id: int, monologue_id: int) -> List[Thought]:
        """Gets the Thoughts of the given Monologue."""
        with self._db.session() as db:
            monologue = self._load_user_monologue(db, user_id, monologue_id)

            res = self.get_monologue_thoughts(monologue.id)
            return list(res)

    def set_monologue_context(self, id: int, context: Dict[str, Any]):
        """Sets the context of the given Monologue."""
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue).where(Monologue.id == id)
            )

            if monologue is None:
                raise NonexistentMonologueError(id)

            monologue.context = context
            db.commit()
    
    def set_monologue_status(self, id: int, status: MonologueStatus):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue).where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)
            
            monologue.status = status
            if monologue.context is not None:
                ctx = copy(monologue.context)
                ctx["FINISHED"] = monologue.is_finished()
                monologue.context = ctx

            db.commit()
    
    def set_monologue_title(self, id: int, title: str):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue).where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)

            monologue.title = title
            db.commit()
    
    def set_monologue_summary(self, id: int, summary: str):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue).where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)

            monologue.summary = summary
            db.commit()
    
    def get_monologue_thoughts(self, id: int):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue)
                .options(
                    joinedload(Monologue.thoughts)
                    .options(
                        joinedload(Thought.invocation).joinedload(Invocation.action),
                        joinedload(Thought.monologue)
                    )
                )
                .where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)
            
            return monologue.thoughts
    
    def get_monologue_thoughts_as_llm_chat_history(self, id: int):
        thoughts = self.get_monologue_thoughts(id)
        res = []
        
        for t in thoughts:
            if t.invocation is not None:
                msg_obj = {
                    "action_name": t.invocation.action.function_name,
                    "arguments": t.invocation.params
                }

                res.append(AssistantMessage(json.dumps(msg_obj)))     
            res.append(UserMessage(t.result))

        return res
    
    def get_monologue_system_prompt(self, id: int):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue)
                .where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)
            
            prompt = monologue.agent.prompt
            allowed_actions = monologue.agent.allowed_actions
            
            for action in allowed_actions:
                desc = self._action.get_action_description(action.id)
                prompt += "\n\n" + desc
                
            return prompt
    
    def get_monologue_by_id(self, id: int):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue)
                .where(Monologue.id == id)
                .options(
                    joinedload(Monologue.agent)
                )
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)
            
            return monologue
    
    def get_monologue_agent_id(self, id: int):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue)
                .where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)
            
            return monologue.agent.id
    
    def append_thought_to_monologue(self, id: int, thought: Thought):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue)
                .where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)
            
            monologue.thoughts.append(thought)
            monologue.modified_at = datetime.now(tz=UTC)
            db.commit()

    def _load_user_monologue(self, db: Session, user_id: int, monologue_id: int):
        res = db.scalar(
            select(Monologue)
            .join(Monologue.agent)
            .where(Agent.owner_id == user_id, Monologue.id == monologue_id)
        )

        if res is None:
            raise NonexistentMonologueError(monologue_id)

        return res
            
        
class NonexistentMonologueError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent monologue id: {id}")
