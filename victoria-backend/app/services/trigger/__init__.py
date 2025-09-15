from app.services.db import DatabaseService
from typing import Dict, Any 
from itertools import chain
from sqlalchemy import select
from app.model.trigger import Trigger, TimerTrigger, PollTrigger, ChatTrigger, WebhookTrigger
from app.model.event import Event
import requests
import re
from threading import Timer

class TriggerService:
    def __init__(
            self,
            database_service: DatabaseService
        ):
        self._db: DatabaseService = database_service
        self._trigger_timers: Dict[int, Timer] = {}
        self.start_stopped_trigger_timers()

    def start_stopped_trigger_timers(self):
        with self._db.session() as db:
            polls = db.scalars(select(PollTrigger))
            timers = db.scalars(select(TimerTrigger))

            timed = chain(polls, timers)

            for trigger in timed:
                timer = Timer(trigger.interval, self._run_trigger_timer, kwargs={
                    "trigger": trigger
                })
                self._trigger_timers[trigger.id] = timer
                timer.start()

    def stop_trigger_timers(self):
        for timer in self._trigger_timers.values():
            timer.cancel()
            timer.join()

        self._trigger_timers.clear()

    def _run_trigger_timer(self, trigger: Trigger):
        interval = 0.0
        if isinstance(trigger, TimerTrigger):
            interval = trigger.interval
            self._execute_timer_trigger(trigger)
        elif isinstance(trigger, PollTrigger):
            interval = trigger.interval
            self._execute_poll_trigger(trigger)
        else:
            raise NotTimedTriggerError(trigger.id)

        new_timer = Timer(interval, self._run_trigger_timer, kwargs={
            "trigger": trigger
        })
        self._trigger_timers[trigger.id] = new_timer
        new_timer.start()

    def _execute_poll_trigger(self, trigger: PollTrigger):
        website_content = ""
        try:
            res = requests.get(trigger.url)
            res.raise_for_status()
            website_content = res.text
        except Exception as e:
            website_content = str(e)

        self.generate_event(trigger.id, {"content": website_content})
    
    def _execute_timer_trigger(self, trigger: TimerTrigger):
        self.generate_event(trigger.id, {})
    
    def receive_chat_message(self, receiver: str, message: str):
        with self._db.session() as db:
            matching = db.scalars(
                select(ChatTrigger)
                .where(ChatTrigger.receiver == receiver)
            )

            for trigger in matching:
                self.generate_event(trigger.id, {"message": message})

    def receive_webhook_payload(self, endpoint: str, content: str):
        with self._db.session() as db:
            matching = db.scalars(
                select(WebhookTrigger)
                .where(WebhookTrigger.endpoint == endpoint)
            )

            for trigger in matching:
                self.generate_event(trigger.id, {"payload": content})


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

class NotTimedTriggerError(Exception):
    def __init__(self, id: int):
        super().__init__(f"trigger with id {id} is not a timed trigger")
