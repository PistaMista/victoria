import pytest
from fastapi.testclient import TestClient
import threading as t
from app.main import create_app

# TODO: Handle event filtering for agents and test the actual full dispatch logic

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

def test_dispatcher_creates_new_monologue_when_an_event_is_added_to_db(client, db_session):
    # Arrange
    trigger = PollTrigger( # A trigger generates events (by polling a website for example)
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)"
    )
    agent = Agent( # An agent processes events
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        # An agent has a whitelist of triggers from which it takes events
        allowed_triggers=[trigger],
        allowed_actions=[]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()

    # Act
    event = Event( # The trigger has generated an event and added it to the DB
        id=42, 
        content="An email has arrived: Hello, this is...", 
        trigger=trigger, 
        # The event starts off in the dispatched=False state by default
        # dispatched=False,
        monologues=[]
    )
    db_session.add(event)
    db_session.commit()
    
    # Assert
    # ...in the case of a new event that has been added, while the dispatcher is running:
    # 1. the event is marked as dispatched
    assert event.dispatched
    # 2. a monologue is created, because an agent with the trigger whitelisted caught the event
    assert len(event.monologues) == 1
    # 3. the monologue is assigned to the agent
    assert event.monologues[0].agent.id == 75
    # 4. the monologue starts off with the event as the first thought
    assert len(event.monologues[0].thoughts) == 1
    assert event.monologues[0].thoughts[0].invocation.event.id == 42
    assert event.monologues[0].thoughts[0].result == "An email has arrived: Hello, this is..."

def test_dispatcher_creates_new_monologue_for_existing_undispatched_events(db_session, app):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)"
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[trigger],
        allowed_actions=[]
    )
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=False,
        monologues=[]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.add(event)
    db_session.commit()

    # Act
    with TestClient(app): # Start and exit the application
        pass
    
    # Assert
    # ...in the case when the application starts up with undispatched events, they are dispatched
    # (the behavior is the same as in the previous case)
    assert event.dispatched
    assert len(event.monologues) == 1
    assert event.monologues[0].agent.id == 75
    assert len(event.monologues[0].thoughts) == 1
    assert event.monologues[0].thoughts[0].invocation.event.id == 42
    assert event.monologues[0].thoughts[0].result == "An email has arrived: Hello, this is..."

    

def test_dispatcher_starts_thread_when_monologue_is_added_to_db(client, db_session):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived..."
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[trigger],
        allowed_actions=[]
    )
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True, # This is dispatched, so no new monologue will be created
        monologues=[]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()

    # Act
    trigger_invocation = TriggerInvocation(
        event=event
    )
    trigger_thought = Thought(
        invocation=trigger_invocation,
        result="An email has arrived..."
    )
    monologue = Monologue(
        title="Process incoming email",
        summary="Thinking",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[
            trigger_thought
        ]
    )
    event.monologues = [ monologue ]
    db_session.add(trigger_invocation)
    db_session.add(trigger_thought)
    db_session.add(monologue)
    db_session.commit()
    
    # Assert
    # ...a fresh thread is started for new monologues
    assert t.active_count() == 4
    
    # Threads are started with the ID of the event, not the monologue
    thread = next((x for x in t.enumerate() if t.name == 'monologue_42'), None)    
    assert thread is not None
    assert thread._args[0].status == MonologueStatus.RUNNING
    assert len(thread._args[0].thoughts) == 1
    assert thread._args[0].thoughts[0].invocation.event.id == 42
    assert thread._args[0].thoughts[0].invocation.event.content == "An email has arrived..."
    assert thread._args[0].thoughts[0].result == "An email has arrived..."


def test_dispatcher_starts_thread_for_existing_unfinished_monologues(db_session, app):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com"
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[trigger],
        allowed_actions=[]
    )
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True,
        monologues=[]
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
        event=event,
        status=MonologueStatus.PENDING,
        thoughts=[
            trigger_thought,
            verbatim_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(trigger)
    db_session.add(event)
    db_session.add(trigger_invocation)
    db_session.add(trigger_thought)
    db_session.add(verbatim_invocation)
    db_session.add(verbatim_thought)
    db_session.add(monologue)
    db_session.commit()
    
    # Act
    with TestClient(app):
        # Assert
        assert t.active_count() == 4
        
        thread = next((x for x in t.enumerate() if t.name == 'monologue_42'), None)    
        assert thread is not None
        assert thread._args[0].status == MonologueStatus.RUNNING
        assert len(thread._args[0].thoughts) == 2
        assert thread._args[0].thoughts[0].invocation.event.id == 42
        assert thread._args[0].thoughts[0].invocation.event.content == "An email has arrived..."
        assert thread._args[0].thoughts[0].result == "An email has arrived..."

        assert thread._args[0].thoughts[1].invocation.content == "I should notify the user of the new email"
        assert thread._args[0].thoughts[1].result == "I should notify the user of the new email"
        
def test_dispatcher_does_nothing_for_finished_monologues():
    # Arrange
    trigger = PollTrigger(name="Emails", url="http://mycooldomain.com")
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True,
        monologues=[]
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
    event.monologues = [ monologue ]
    
    db_session.add(trigger)
    db_session.add(event)
    db_session.add(trigger_invocation)
    db_session.add(trigger_thought)
    db_session.add(success_invocation)
    db_session.add(success_invocation)
    db_session.add(monologue)
    db_session.commit()

    # Act
    with TestClient(app):
        # Assert
        assert t.active_count() == 3
        
        thread = next((x for x in t.enumerate() if t.name == 'monologue_42'), None)    
        assert thread is None