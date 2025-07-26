import pytest
from fastapi.testclient import TestClient
import threading as t
from app.main import create_app

def test_dispatcher_starts_when_application_constructed(app):
    # Arrange
    assert t.active_count() == 1

    # Act
    with TestClient(app):
    
        # Assert
        assert t.active_count() == 3
        assert 'dispatcher' in [x.name for x in t.enumerate()]

def test_dispatcher_stops_when_application_destroyed(app):
    # Arrange

    # Act
    with TestClient(app):
        assert t.active_count() == 3
    
    # Assert
    assert t.active_count() == 1
    assert 'dispatcher' not in [x.name for x in t.enumerate()]

def test_dispatcher_creates_new_monologue_when_an_event_is_added_to_db(client, db_connection):
    # Arrange
    trigger = PollTrigger(name="Emails", url="http://mycooldomain.com")
    db_session.add(trigger)
    db_session.flush()

    # Act
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        monologue=None
    )
    db_session.add(event)
    db_session.flush()
    
    # Assert
    db_connection.expire(event, ['monologue'])
    assert event.monologue is not None
    assert len(event.monologue.thoughts) == 1
    assert event.monologue.thoughts[0].invocation.event.id == 42
    assert event.monologue.thoughts[0].result == "An email has arrived"

def test_dispatcher_creates_new_monologue_for_existing_events_with_no_monologue(db_session, app):
    # Arrange
    trigger = PollTrigger(name="Emails", url="http://mycooldomain.com")
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        monologue=None
    )
    db_session.add(trigger)
    db_session.add(event)
    db_session.flush()

    # Act
    with TestClient(app):
        pass
    
    # Assert
    db_connection.expire(event, ['monologue'])
    assert event.monologue is not None
    assert len(event.monologue.thoughts) == 1
    assert event.monologue.thoughts[0].invocation.event.id == 42
    assert event.monologue.thoughts[0].result == "An email has arrived"

    

def test_dispatcher_starts_thread_with_new_monologue_when_an_event_is_added_to_db(client, db_session):
    # Arrange
    trigger = PollTrigger(name="Emails", url="http://mycooldomain.com")
    db_session.add(trigger)
    db_session.flush()

    # Act
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        monologue=None
    )
    db_session.add(event)
    db_session.flush()
    
    # Assert
    assert t.active_count() == 4
    
    # Threads are started with the ID of the event, not the monologue
    thread = next((x for x in t.enumerate() if t.name == 'monologue_42'), None)    
    assert thread is not None
    assert len(thread._args[0].thoughts) == 1
    assert thread._args[0].thoughts[0].invocation.event.id == 42
    assert thread._args[0].thoughts[0].invocation.event.content == "An email has arrived..."
    assert thread._args[0].thoughts[0].result == "An email has arrived..."


def test_dispatcher_starts_thread_with_new_monologue_for_existing_events_with_no_monologue(db_session, app):
    # Arrange
    trigger = PollTrigger(name="Emails", url="http://mycooldomain.com")
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        monologue=None
    )
    db_session.add(trigger)
    db_session.add(event)
    db_session.flush()

    # Act
    with TestClient(app):
        # Assert
        assert t.active_count() == 4
        
        thread = next((x for x in t.enumerate() if t.name == 'monologue_42'), None)    
        assert thread is not None
        assert len(thread._args[0].thoughts) == 1
        assert thread._args[0].thoughts[0].invocation.event.id == 42
        assert thread._args[0].thoughts[0].invocation.event.content == "An email has arrived..."
        assert thread._args[0].thoughts[0].result == "An email has arrived..."
    

def test_dispatcher_starts_thread_with_old_monologue_for_existing_events_when_unfinished(db_session, app):
    # Arrange
    trigger = PollTrigger(name="Emails", url="http://mycooldomain.com")
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        monologue=None
    )
    trigger_invocation = TriggerInvocation(
        event=event
    )
    trigger_thought = Thought(
        invocation=trigger_invocation,
        result="An email has arrived..."
    )
    verbatim_invocation = ThoughtInvocation(
        content="I should notify the user of the new email"
    )
    verbatim_thought = Thought(
        invocation=verbatim_invocation,
        result="I should notify the user of the new email"
    )
    monologue = Monologue(
        title="Handle incoming email",
        summary="Thinking",
        status=MonologueStatus.PENDING,
        thoughts=[
            trigger_thought,
            verbatim_thought
        ]
    )
    event.monologue = monologue
    
    db_session.add(trigger)
    db_session.add(event)
    db_session.add(trigger_invocation)
    db_session.add(trigger_thought)
    db_session.add(verbatim_invocation)
    db_session.add(verbatim_thought)
    db_session.add(monologue)
    db_session.flush()
    
    # Act
    with TestClient(app):
        # Assert
        assert t.active_count() == 4
        
        thread = next((x for x in t.enumerate() if t.name == 'monologue_42'), None)    
        assert thread is not None
        assert len(thread._args[0].thoughts) == 2
        assert thread._args[0].thoughts[0].invocation.event.id == 42
        assert thread._args[0].thoughts[0].invocation.event.content == "An email has arrived..."
        assert thread._args[0].thoughts[0].result == "An email has arrived..."

        assert thread._args[0].thoughts[1].invocation.content == "I should notify the user of the new email"
        assert thread._args[0].thoughts[1].result == "I should notify the user of the new email"
        
def test_dispatcher_does_nothing_for_finished_events():
    # Arrange
    trigger = PollTrigger(name="Emails", url="http://mycooldomain.com")
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        monologue=None
    )
    trigger_invocation = TriggerInvocation(
        event=event
    )
    trigger_thought = Thought(
        invocation=trigger_invocation,
        result="An email has arrived..."
    )
    success_invocation = SuccessInvocation()
    success_thought = Thought(
        invocation=success_invocation,
        result="I should notify the user of the new email"
    )
    monologue = Monologue(
        title="Handle incoming email",
        summary="Thinking",
        status=MonologueStatus.SUCCESS,
        thoughts=[
            trigger_thought,
            success_invocation
        ]
    )
    event.monologue = monologue
    
    db_session.add(trigger)
    db_session.add(event)
    db_session.add(trigger_invocation)
    db_session.add(trigger_thought)
    db_session.add(success_invocation)
    db_session.add(success_invocation)
    db_session.add(monologue)
    db_session.flush()

    # Act
    with TestClient(app):
        # Assert
        assert t.active_count() == 3
        
        thread = next((x for x in t.enumerate() if t.name == 'monologue_42'), None)    
        assert thread is None