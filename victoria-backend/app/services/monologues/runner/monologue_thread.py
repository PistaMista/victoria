import threading
from typing import Callable
from app.model.monologue import Monologue, MonologueStatus
from app.model.thought import Thought
from app.services.monologues import MonologueService
from app.services.llm import LLMService, SystemMessage
from app.services.action import ActionService
from datetime import datetime, UTC

class MonologueThread(threading.Thread):
    def __init__(
        self,
        monologue_id: int,
        on_finish: Callable[['MonologueThread'], None]
    ):
        super().__init__(name=f"monologue_{monologue_id}")
        self._id: int = monologue_id
        self._on_finish: Callable[['MonologueThread'], None] = on_finish
    

class AgenticMonologueThread(MonologueThread):
    def __init__(
        self,
        monologue_id: int,
        on_finish: Callable[['MonologueThread'], None],
        monologue_service: MonologueService,
        llm_service: LLMService,
        action_service: ActionService
    ):
        super().__init__(
            monologue_id=monologue_id,
            on_finish=on_finish
        )
        
        self._monologue: MonologueService = monologue_service
        self._llm: LLMService = llm_service
        self._action: ActionService = action_service
    
    def run(self):
        try:
            monologue = self._monologue.get_monologue_by_id(self._id)
            while not monologue.is_finished():
                self.do_iteration()
                monologue = self._monologue.get_monologue_by_id(self._id)
        except:
            try:
                self._monologue.set_monologue_status(self._id, MonologueStatus.FAILURE)
            finally:
                pass
        finally:
            self._on_finish(self)

    
    def do_iteration(self):
        monologue = self._monologue.get_monologue_by_id(self._id)
        thoughts = self._monologue.get_monologue_thoughts_as_llm_chat_history(self._id)
        prompt = self._monologue.get_monologue_system_prompt(self._id)
        model_id = monologue.agent.model_id
        context = monologue.context or { }
        
        thoughts.insert(0, SystemMessage(prompt))
        
        llm_response = self._llm.get_chat_completion(model_id, thoughts)
        
        invocation = self._action.parse_invocation(llm_response._content)
        result = self._action.execute_invocation(invocation, context)
        
        # TODO: Check if the called action is allowed, since the action service does not check this
        
        new_thought = Thought(
            timestamp=datetime.now(tz=UTC),
            invocation=invocation,
            result=result
        )
        
        self._monologue.append_thought_to_monologue(self._id, new_thought)
        self._monologue.set_monologue_context(self._id, context)
