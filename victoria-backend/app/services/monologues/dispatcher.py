from sqlalchemy import event, select, or_
from sqlalchemy.orm import sessionmaker, Session
from app.model.event import Event
from app.model.thought import Thought
from app.model.monologue import Monologue, MonologueStatus
from app.services.db import DatabaseService
from app.services.monologues.runner import RunnerService
from datetime import datetime, timezone

class DispatcherService:
    def __init__(
        self, 
        db_service: DatabaseService,
        runner_service: RunnerService
    ):
        self._db = db_service
        self._runner = runner_service

    def stop(self):
        event.remove(Session, 'after_commit', self.after_commit)
        event.remove(Session, 'before_commit', self.before_commit)

    def start(self):
        event.listen(Session, 'before_commit', self.before_commit)
        event.listen(Session, 'after_commit', self.after_commit)
        self.dispatch_undispatched_events()
        self.restart_unfinished_monologues()


    def before_commit(self, session: Session):
        session._new_events = [ e for e in session.new if isinstance(e, Event) ]
        session._new_monologues = [ m for m in session.new if isinstance(m, Monologue) ]
    
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
                trigger_thought = Thought(
                    timestamp=datetime.now(tz=timezone.utc),
                    invocation=None,
                    result=event.content
                )
                new_monologue = Monologue(
                    title="Untitled",
                    summary="No summary",
                    event=event,
                    agent=agent,
                    status=MonologueStatus.PENDING,
                    thoughts=[
                        trigger_thought
                    ]
                )
                db.add(trigger_thought)
                db.add(new_monologue)
                
            event.dispatched = True
            db.commit()
    
    def start_monologue_thread(self, monologue: Monologue):
        with self._db.session() as db:
            monologue = db.scalar(
                select(Monologue).where(Monologue.id == monologue.id)
            )
            
            if monologue is None:
                return
            
            monologue.status = MonologueStatus.RUNNING
            self._runner.start_monologue_process(monologue.id)
            db.commit()
