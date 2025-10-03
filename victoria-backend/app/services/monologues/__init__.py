from app.services.db import DatabaseService
from app.services.action import ActionService
from app.services.llm import UserMessage, AssistantMessage
from app.model.monologue import Monologue, MonologueStatus
from app.model.thought import Thought
from app.model.invocation import Invocation
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import json

class MonologueService:
    def __init__(
        self,
        database_service: DatabaseService,
        action_service: ActionService
    ):
        self._db: DatabaseService = database_service
        self._action: ActionService = action_service

    def get_user_monologues(self, user_id: int) -> List[Monologue]:
        """Gets all of the given User's monologues."""
        pass

    def get_user_monologue(self, user_id: int, monologue_id: int) -> Monologue:
        """Gets the given Monologue."""
        pass

    def end_user_monologue(self, user_id: int, monologue_id: int, successful: bool):
        """Ends the given Monologue with either SUCCESS or FAILURE."""
        pass

    def get_user_monologue_thoughts(self, user_id: int, monologue_id: int) -> List[Thought]:
        """Gets the Thoughts of the given Monologue."""
        pass
    
    def set_monologue_status(self, id: int, status: MonologueStatus):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue).where(Monologue.id == id)
            )
            
            if monologue is None:
                raise NonexistentMonologueError(id)
            
            monologue.status = status
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
                    .joinedload(Thought.invocation)
                    .joinedload(Invocation.action)
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
            db.commit()
            
        
class NonexistentMonologueError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent monologue id: {id}")
