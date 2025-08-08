import threading
from typing import Generator
from contextlib import contextmanager
from sqlalchemy import event, select
from sqlalchemy.orm import sessionmaker, Session
from app.model.event import Event
from app.model.invocation import TriggerInvocation
from app.model.thought import Thought
from app.model.monologue import Monologue, MonologueStatus

class Dispatcher:
    def __init__(self, db_generator: Generator[Session, None, None]):
        self.monologue_threads: [threading.Thread] = []
        self.db_generator: Generator[Session, None, None] = db_generator

    def stop(self):
        event.remove(Session, 'after_commit', self.after_commit)
        event.remove(Session, 'before_commit', self.before_commit)

        for t in self.monologue_threads:
            t.join(timeout=1.0)

    def start(self):
        event.listen(Session, 'before_commit', self.before_commit)
        event.listen(Session, 'after_commit', self.after_commit)
        self.dispatch_undispatched_events()


    def before_commit(self, session: Session):
        session._new_events = [ e for e in session.new if isinstance(e, Event) ]
    
    def dispatch_undispatched_events(self):
        session = self.get_db()
        events = session.scalars(
            select(Event).where(not Event.dispatched)
        )
        
        for event in events:
            self.on_event_added(event)
        
        
    def after_commit(self, session: Session):
        for event in session._new_events:
            self.on_event_added(event)

    def on_event_added(self, event: Event):
        session = self.get_db()
        event = session.scalars(
            select(Event).where(Event.id == event.id)
        ).first()
        
        if event is None:
            return

        matching_agents = event.trigger.allowed_on_agents
        for agent in matching_agents:
            trigger_invocation = TriggerInvocation(
                event=event
            )
            trigger_thought = Thought(
                invocation=trigger_invocation,
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
            session.add(trigger_invocation)
            session.add(trigger_thought)
            session.add(new_monologue)
            
        event.dispatched = True
        session.commit()
        session.close()

def monologue_thread():
    threading.Event().wait()
