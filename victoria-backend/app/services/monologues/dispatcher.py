from sqlalchemy import event, select, or_, exists
from sqlalchemy.orm import Session
from base64 import b64encode
from app.model.event import Event
from app.model.thought import Thought
from app.model.monologue import Monologue, MonologueStatus
from app.services.db import DatabaseService
from app.services.monologues.runner import RunnerService
from datetime import datetime, timezone
import os

class DispatcherService:
    def __init__(
        self, 
        db_service: DatabaseService,
        runner_service: RunnerService,
        base_url: str
    ):
        self._db = db_service
        self._runner = runner_service
        self._base_url = base_url

    def stop(self):
        event.remove(Session, 'after_commit', self.after_commit)
        event.remove(Session, 'before_flush', self.before_flush)

    def start(self):
        event.listen(Session, 'before_flush', self.before_flush)
        event.listen(Session, 'after_commit', self.after_commit)
        self.dispatch_undispatched_events()
        self.restart_unfinished_monologues()


    def before_flush(self, session: Session, context, instances):
        if not hasattr(session, "_new_events"):
            session._new_events = []

        if not hasattr(session, "_new_monologues"):
            session._new_monologues = []

        session._new_events.extend([ e for e in session.new if isinstance(e, Event) and e not in session._new_events])
        session._new_monologues.extend([ m for m in session.new if isinstance(m, Monologue) and m not in session._new_monologues])
    
    def after_commit(self, session: Session):
        for event in session._new_events:
            self.on_event_added(event)
        
        for monologue in session._new_monologues:
            self.start_monologue_thread(monologue)

    def dispatch_undispatched_events(self):
        with self._db.session() as db:
            events = db.scalars(
                select(Event).where(Event.dispatched == False)
            )
        
            for event in events:
                self.on_event_added(event)
    
    def restart_unfinished_monologues(self):
        with self._db.session() as db:
            monologues = db.scalars(
                select(Monologue).where(
                    or_(
                        Monologue.status == MonologueStatus.PENDING,
                        Monologue.status == MonologueStatus.RUNNING
                    )
                )
            )
            
            for monologue in monologues:
                self.start_monologue_thread(monologue)

    def on_event_added(self, event: Event):
        with self._db.session() as db:
            event = db.scalars(
                select(Event).where(Event.id == event.id)
            ).first()
            
            if event is None:
                return

            matching_agents = event.trigger.allowed_on_agents
            for agent in matching_agents:
                now = datetime.now(tz=timezone.utc)
                trigger_thought = Thought(
                    timestamp=now,
                    invocation=None,
                    result=event.content
                )
                new_monologue = Monologue(
                    title="Untitled",
                    summary="No summary",
                    event=event,
                    agent=agent,
                    dispatched_at=now,
                    modified_at=now,
                    status=MonologueStatus.PENDING,
                    thoughts=[
                        trigger_thought
                    ]
                )
                db.add(trigger_thought)
                db.add(new_monologue)

                # Generate an agent token
                while new_monologue.agent_token is None:
                    new_token = os.urandom(32)

                    taken = db.scalar(
                        select(exists().where(Monologue.agent_token == new_token))
                    )

                    if taken:
                        continue

                    new_monologue.agent_token = new_token

                db.flush() # So new_monologue.id is available
                new_monologue.context = {
                    "FINISHED": False,
                    "BASE_URL": self._base_url,
                    "MONOLOGUE_ID": new_monologue.id,
                    "AGENT_ID": agent.id,
                    "TOKEN": b64encode(new_monologue.agent_token).decode("utf-8")
                }

                
            event.dispatched = True
            db.commit()
    
    def start_monologue_thread(self, monologue: Monologue):
        print(f"Starting monologue #{monologue.id}")
        self._runner.start_monologue_process(monologue.id)
