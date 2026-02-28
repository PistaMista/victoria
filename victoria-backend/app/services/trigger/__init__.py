from app.services.db import DatabaseService
from typing import Dict, Any, Optional, Literal, List
from itertools import chain
from sqlalchemy import select
from sqlalchemy.orm import joinedload, with_polymorphic, undefer, make_transient
from sqlalchemy.inspection import inspect
from app.model.user import User
from app.model.trigger import (
    Trigger,
    TimerTrigger,
    PollTrigger,
    ChatTrigger,
    WebhookTrigger,
)
from app.model.event import Event
from pydantic import BaseModel
import requests
import re
from threading import Timer


class TriggerService:
    def __init__(self, database_service: DatabaseService):
        self._db: DatabaseService = database_service
        self._trigger_timers: Dict[int, Timer] = {}
        self.start_stopped_trigger_timers()

    def get_user_event(self, user_id: int, event_id: int) -> Event:
        """Gets the given Event."""
        with self._db.session() as db:
            res = db.scalar(
                select(Event)
                .join(Event.trigger)
                .join(Trigger.allowed_on_users)
                .where(Event.id == event_id, User.id == user_id)
                .options(joinedload(Event.trigger))
            )

            if res is None:
                raise NonexistentEventError(event_id)

            return res

    def get_user_allowed_triggers(self, user_id: int) -> List[Trigger]:
        """Gets all the Triggers allowed for the User's Agents."""
        with self._db.session() as db:
            res = db.scalars(
                select(Trigger).join(Trigger.allowed_on_users).where(User.id == user_id)
            ).all()

            return res

    def get_all_triggers(self) -> List[Trigger]:
        """Gets all available Triggers."""
        with self._db.session() as db:
            res = db.scalars(select(Trigger).order_by(Trigger.id.asc())).all()

            return res

    def add_timer_trigger(self, name: str, template: str, interval: int) -> int:
        """Creates a new timer trigger and returns its id."""
        with self._db.session() as db:
            new = TimerTrigger(name=name, template=template, interval=interval)

            db.add(new)
            db.commit()

            self.restart_trigger_timer(trigger_id=new.id)
            return new.id

    def add_poll_trigger(
        self, name: str, template: str, interval: int, url: str
    ) -> int:
        """Creates a new poll trigger and returns its id."""
        with self._db.session() as db:
            new = PollTrigger(name=name, template=template, interval=interval, url=url)

            db.add(new)
            db.commit()

            self.restart_trigger_timer(trigger_id=new.id)
            return new.id

    def add_chat_trigger(self, name: str, template: str, receiver: str) -> int:
        """Creates a new chat trigger and returns its id."""
        with self._db.session() as db:
            new = ChatTrigger(name=name, template=template, receiver=receiver)

            db.add(new)
            db.commit()

            return new.id

    def add_webhook_trigger(self, name: str, template: str, endpoint: str) -> int:
        """Creates a new webhook trigger and returns its id."""
        with self._db.session() as db:
            new = WebhookTrigger(name=name, template=template, endpoint=endpoint)

            db.add(new)
            db.commit()

            return new.id

    def get_trigger_by_id(self, id: int) -> Trigger:
        """Gets the given Trigger."""
        with self._db.session() as db:
            TriggerPoly = with_polymorphic(
                base=Trigger,
                classes=[ChatTrigger, PollTrigger, TimerTrigger, WebhookTrigger],
            )
            res = db.scalar(
                select(TriggerPoly)
                .where(Trigger.id == id)
                .options(
                    undefer(TriggerPoly.template),
                    undefer(TriggerPoly.ChatTrigger.receiver),
                    undefer(TriggerPoly.PollTrigger.url),
                    undefer(TriggerPoly.WebhookTrigger.endpoint),
                )
            )

            if res is None:
                raise NonexistentTriggerError(id)

            return res

    def update_trigger(self, trigger_id: int, changes: "TriggerDiff"):
        """Updates the given Trigger."""

        with self._db.session() as db:
            with db.no_autoflush:
                old = db.scalar(select(Trigger).where(Trigger.id == trigger_id))
                new = old

                if old is None:
                    raise NonexistentTriggerError(trigger_id)

                # Store old relationships
                rel_data = {}
                for rel in inspect(Trigger).relationships:
                    rel_data[rel.key] = getattr(old, rel.key)

                # Apply type-specific changes by creating a new trigger instance
                match (old, changes):
                    case (TimerTrigger(), TimerTriggerDiff()):
                        new = TimerTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            interval=changes.interval or old.interval,
                        )
                    case (Trigger(), TimerTriggerDiff()):
                        new = TimerTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            interval=changes.interval or 3600,
                        )
                    case (PollTrigger(), PollTriggerDiff()):
                        new = PollTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            interval=changes.interval or old.interval,
                            url=changes.url or old.url,
                        )
                    case (Trigger(), PollTriggerDiff()):
                        new = PollTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            interval=changes.interval or 3600,
                            url=changes.url or "",
                        )
                    case (ChatTrigger(), ChatTriggerDiff()):
                        new = ChatTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            receiver=changes.receiver or old.receiver,
                        )
                    case (Trigger(), ChatTriggerDiff()):
                        new = ChatTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            receiver=changes.receiver or "",
                        )
                    case (WebhookTrigger(), WebhookTriggerDiff()):
                        new = WebhookTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            endpoint=changes.endpoint or old.endpoint,
                        )
                    case (Trigger(), WebhookTriggerDiff()):
                        new = WebhookTrigger(
                            id=old.id,
                            name=old.name,
                            template=old.template,
                            endpoint=changes.endpoint or "",
                        )

                # Apply base changes
                if changes.name is not None:
                    new.name = changes.name

                if changes.template is not None:
                    new.template = changes.template

                if new is not old:
                    db.delete(old)
                    db.flush()

                    # Restore relationships
                    for key, value in rel_data.items():
                        setattr(new, key, value)

                    db.add(new)

                db.commit()

                if isinstance(new, TimerTrigger) or isinstance(new, PollTrigger):
                    self.restart_trigger_timer(trigger_id=new.id)

    def remove_trigger(self, id: int):
        """Deletes the given Trigger."""
        with self._db.session() as db:
            trigger = db.scalar(select(Trigger).where(Trigger.id == id))

            if trigger is None:
                raise NonexistentTriggerError(id)

            if isinstance(trigger, TimerTrigger) or isinstance(trigger, PollTrigger):
                self.stop_trigger_timer(trigger_id=trigger.id)

            db.delete(trigger)
            db.commit()

    def start_stopped_trigger_timers(self):
        with self._db.session() as db:
            polls = db.scalars(select(PollTrigger))
            timers = db.scalars(select(TimerTrigger))

            timed = chain(polls, timers)

            for trigger in timed:
                self.restart_trigger_timer(trigger.id)

    def stop_trigger_timers(self):
        for timer in self._trigger_timers.values():
            timer.cancel()
            timer.join()

        self._trigger_timers.clear()

    def restart_trigger_timer(self, trigger_id: int):
        """Restarts the specified trigger's timer if running or starts it if stopped."""
        with self._db.session() as db:
            trigger = db.scalar(select(Trigger).where(Trigger.id == trigger_id))

            if not isinstance(trigger, TimerTrigger) and not isinstance(
                trigger, PollTrigger
            ):
                raise NonexistentTriggerError(trigger_id)

            if trigger.id in self._trigger_timers:
                timer = self._trigger_timers[trigger.id]
                timer.cancel()
                timer.join()

            timer = Timer(
                trigger.interval, self._run_trigger_timer, kwargs={"trigger": trigger}
            )
            self._trigger_timers[trigger.id] = timer
            timer.start()

    def stop_trigger_timer(self, trigger_id: int):
        """Stops the specified trigger's timer if running."""
        with self._db.session() as db:
            trigger = db.scalar(select(Trigger).where(Trigger.id == trigger_id))

            if not isinstance(trigger, TimerTrigger) and not isinstance(
                trigger, PollTrigger
            ):
                raise NonexistentTriggerError(trigger_id)

            if trigger.id in self._trigger_timers:
                timer = self._trigger_timers[trigger.id]
                timer.cancel()
                timer.join()

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

        new_timer = Timer(
            interval, self._run_trigger_timer, kwargs={"trigger": trigger}
        )
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

    def receive_chat_message(
        self,
        receiver: str,
        message: str,
        chat_id: Optional[int] = None,
        exchange_id: Optional[int] = None,
    ) -> List[int]:
        with self._db.session() as db:
            matching = db.scalars(
                select(ChatTrigger).where(ChatTrigger.receiver == receiver)
            )

            return [
                self.generate_event(
                    trigger.id,
                    {"message": message, "chatId": chat_id, "exchangeId": exchange_id},
                )
                for trigger in matching
            ]

    def receive_webhook_payload(self, endpoint: str, content: str):
        # TODO: Make this method raise InvalidWebhookEndpointError when no matching endpoint is found
        with self._db.session() as db:
            matching = db.scalars(
                select(WebhookTrigger).where(WebhookTrigger.endpoint == endpoint)
            )

            for trigger in matching:
                self.generate_event(trigger.id, {"payload": content})

    def generate_event(self, trigger_id: int, variables: Dict[str, Any]) -> int:
        trigger = None
        with self._db.session() as db:
            trigger = db.scalar(select(Trigger).where(Trigger.id == trigger_id))

        if trigger is None:
            raise NonexistentTriggerError(trigger_id)

        used_variables = re.findall(r"\$\(([^)]+)\)", trigger.template)

        res = trigger.template
        for var in used_variables:
            value = str(variables.get(var, ""))
            res = res.replace(f"$({var})", value)

        with self._db.session() as db:
            event = Event(trigger_id=trigger.id, content=res, dispatched=False)
            db.add(event)
            db.commit()

            return event.id


class TriggerDiff(BaseModel):
    name: Optional[str] = None
    parser: Optional[Literal["identity"]] = None
    template: Optional[str] = None


class TimerTriggerDiff(TriggerDiff):
    interval: Optional[int] = None


class PollTriggerDiff(TriggerDiff):
    interval: Optional[int] = None
    url: Optional[str] = None


class ChatTriggerDiff(TriggerDiff):
    receiver: Optional[str] = None


class WebhookTriggerDiff(TriggerDiff):
    endpoint: Optional[str] = None


class InvalidWebhookEndpointError(Exception):
    def __init__(self, endpoint: str):
        super().__init__(f"invalid webhook endpoint: {endpoint}")


class NonexistentTriggerError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent trigger with id: {id}")


class NonexistentEventError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent event with id: {id}")


class NotTimedTriggerError(Exception):
    def __init__(self, id: int):
        super().__init__(f"trigger with id {id} is not a timed trigger")
