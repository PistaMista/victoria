from app.services.db import DatabaseService
from typing import Dict, Any
from sqlalchemy import select
from app.model.trigger import Trigger
from app.model.event import Event
import re

class TriggerService:
    def __init__(
            self,
            database_service: DatabaseService
        ):
        self._db: DatabaseService = database_service
        self.start_stopped_trigger_timers()

    def start_stopped_trigger_timers(self):
        pass

    def stop_trigger_timers(self):
        pass

    def generate_event(self, trigger_id: int, variables: Dict[str, Any]):
        trigger = None
        with self._db.session() as db:
            trigger = db.scalar(
                select(Trigger).where(Trigger.id == trigger_id)
            )

        if trigger is None:
            raise NonexistentTriggerError(trigger_id)


        used_variables = re.findall(r"\$\(([^)]+)\)", trigger.template)

        res = trigger.template
        for var in used_variables:
            value = str(variables.get(var, ""))
            res = res.replace(f"$({var})", value)

        with self._db.session() as db:
            event = Event(
                trigger_id=trigger.id,
                content=res,
                dispatched=False
            )
            db.add(event)
            db.commit()
        

class NonexistentTriggerError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent trigger with id: {id}")
