import pytest
from unittest import mock
from base64 import b64encode
from sqlalchemy import select
from app.model.user import User, Role
from app.model.agent import Agent
from app.model.event import Event
from app.model.monologue import Monologue, MonologueStatus
from app.model.thought import Thought
from app.model.action import Action
from app.model.action_repository import ActionRepository
from app.model.invocation import Invocation
from app.model.trigger import PollTrigger
from app.services.db import DatabaseService
from app.services.monologues.dispatcher import DispatcherService
from datetime import datetime, UTC

@pytest.fixture(scope="function")
def runner():
    return mock.MagicMock()

@pytest.fixture(scope="function")
def dispatcher(db_container, runner, db_factory):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield DispatcherService(
            db_service=db,
            runner_service=runner,
            base_url="golem:11435"
        )

@pytest.fixture(scope="function")
def owner():
    return User(
        username="John",
        password_hash="",
        role=Role.USER
    )

@mock.patch("app.services.monologues.dispatcher.datetime")
def test_dispatcher_creates_new_monologue_when_an_event_is_added_to_db(mock_datetime, db_session, dispatcher, owner):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(5000, tz=UTC)
    trigger = PollTrigger( # A trigger generates events (by polling a website for example)
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent( # An agent processes events
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        # An agent has a whitelist of triggers from which it takes events
        allowed_triggers=[trigger]
        # allowed_actions=[]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()

    # Act
    dispatcher.start()
    event = Event( # The trigger has generated an event and added it to the DB
        id=42, 
        content="An email has arrived: Hello, this is...", 
        trigger=trigger, 
        dispatched=False, # Each event is created with dispatched=False
        monologues=[]
    )
    db_session.add(event)
    db_session.commit()
    dispatcher.stop()
    
    # Assert
    # ...in the case of a new event that has been added, while the dispatcher is running:
    # 1. the event is marked as dispatched
    assert event.dispatched
    # 2. a monologue is created, because an agent with the trigger whitelisted caught the event
    assert len(event.monologues) == 1
    # 3. the monologue is assigned to the agent
    assert event.monologues[0].agent.id == 75
    # 4. the monologue is given a dispatch time
    assert event.monologues[0].dispatched_at == datetime.fromtimestamp(5000, tz=UTC)
    assert event.monologues[0].modified_at == datetime.fromtimestamp(5000, tz=UTC)
    # 5. the monologue starts off with the event as the first thought
    assert len(event.monologues[0].thoughts) == 1
    assert event.monologues[0].thoughts[0].invocation is None
    assert event.monologues[0].thoughts[0].result == "An email has arrived: Hello, this is..."


@mock.patch("app.services.monologues.dispatcher.datetime")
def test_dispatcher_creates_new_monologue_for_existing_undispatched_events(mock_datetime, db_session, dispatcher, owner):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(5000, tz=UTC)
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
        # allowed_actions=[]
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
    dispatcher.start()
    dispatcher.stop()
    
    # Assert
    # ...in the case when the application starts up with undispatched events, they are dispatched
    # (the behavior is the same as in the previous case)
    assert event.dispatched
    assert len(event.monologues) == 1
    assert event.monologues[0].agent.id == 75
    assert event.monologues[0].dispatched_at == datetime.fromtimestamp(5000, tz=UTC)
    assert event.monologues[0].modified_at == datetime.fromtimestamp(5000, tz=UTC)
    assert len(event.monologues[0].thoughts) == 1
    assert event.monologues[0].thoughts[0].invocation is None
    assert event.monologues[0].thoughts[0].result == "An email has arrived..."

def test_dispatcher_sets_basic_monologue_context_when_dispatching_monologue(db_session, dispatcher, owner):
    # Arrange
    trigger = PollTrigger( 
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent( 
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()

    # Act
    dispatcher.start()
    event = Event( 
        id=42, 
        content="An email has arrived: Hello, this is...", 
        trigger=trigger, 
        dispatched=False, 
        monologues=[]
    )
    db_session.add(event)
    db_session.commit()
    dispatcher.stop()
    
    # Assert
    assert event.monologues[0].context["FINISHED"] == False
    assert event.monologues[0].context["MONOLOGUE_ID"] == event.monologues[0].id
    assert event.monologues[0].context["BASE_URL"] == "golem:11435"

@mock.patch("app.services.monologues.dispatcher.os.urandom")
def test_dispatcher_sets_monologue_agent_token_when_dispatching_monologue(mock_urandom, db_session, dispatcher, owner):
    # Arrange
    mock_urandom.return_value = b'aaaa'
    trigger = PollTrigger( 
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent( 
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()

    # Act
    dispatcher.start()
    event = Event( 
        id=42, 
        content="An email has arrived: Hello, this is...", 
        trigger=trigger, 
        dispatched=False, 
        monologues=[]
    )
    db_session.add(event)
    db_session.commit()
    dispatcher.stop()

    # Act
    assert event.monologues[0].agent_token == b'aaaa'
    assert event.monologues[0].context["TOKEN"] == b64encode(b'aaaa').decode("utf-8")

@mock.patch("app.services.monologues.dispatcher.os.urandom")
def test_dispatcher_generates_monologue_context_token_again_after_token_collision_when_dispatching_monologue(mock_urandom, db_session, dispatcher, owner):
    # Arrange
    mock_urandom.side_effect = [b'aaaa', b'bbbb']
    trigger = PollTrigger( 
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent( 
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
    )
    existing_event = Event(
        id=50,
        content="W",
        trigger=trigger,
        dispatched=True
    )
    existing_monologue = Monologue(
        status=MonologueStatus.PENDING,
        event=existing_event,
        agent=agent,
        agent_token=b'aaaa'
    )

    db_session.add(trigger)
    db_session.add(agent)
    db_session.add(existing_monologue)
    db_session.commit()

    # Act
    dispatcher.start()
    event = Event( 
        id=42, 
        content="An email has arrived: Hello, this is...", 
        trigger=trigger, 
        dispatched=False, 
        monologues=[]
    )
    db_session.add(event)
    db_session.commit()
    dispatcher.stop()

    # Act
    assert event.monologues[0].agent_token == b'bbbb'
    assert event.monologues[0].context["TOKEN"] == b64encode(b'bbbb').decode("utf-8")

def test_dispatcher_does_nothing_for_dispatched_events(db_session, dispatcher, owner):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
        # allowed_actions=[]
    )
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True, # Already dispatched
        monologues=[]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.add(event)
    db_session.commit()

    # Act
    dispatcher.start()
    dispatcher.stop()

    # Assert
    # ...in this case the event has already been processed, so no new monologues should have been created
    assert len(event.monologues) == 0
    assert db_session.scalars(select(Monologue)).first() is None
    
def test_dispatcher_does_not_create_monologues_for_new_events_with_no_matching_agent(dispatcher, db_session, owner):
    # Arrange
    trigger = PollTrigger( # A trigger generates events (by polling a website for example)
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent( # An agent processes events
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        # The trigger whitelist is empty - no monologues can start
        allowed_triggers=[]
        # allowed_actions=[]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()
    
    # Act
    dispatcher.start()
    event = Event( # The trigger has generated an event and added it to the DB
        id=42, 
        content="An email has arrived: Hello, this is...", 
        trigger=trigger, 
        dispatched=False,
        monologues=[]
    )
    db_session.add(event)
    db_session.commit()
    dispatcher.stop()

    # Assert
    # ...in this case the event is not picked up by any agent (but is marked as dispatched)
    assert event.dispatched
    assert len(event.monologues) == 0
    assert db_session.scalars(select(Monologue)).first() is None

def test_dispatcher_does_not_create_monologues_for_existing_undispatched_events_with_no_matching_agent(dispatcher, db_session, owner):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[]
        # allowed_actions=[]
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
    dispatcher.start()
    dispatcher.stop()

    # Assert
    # ...in this case the event is not picked up by any agent (but is marked as dispatched)
    assert event.dispatched
    assert len(event.monologues) == 0
    assert db_session.scalars(select(Monologue)).first() is None


def test_dispatcher_instructs_runner_to_start_processing_when_monologue_is_added_to_db(dispatcher, runner, db_session, owner):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived...",
        interval=600
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[trigger],
        owner=owner
        # allowed_actions=[]
    )
    event = Event(
        id=2, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True, # This is dispatched, so no new monologue will be created
        monologues=[]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()

    # Act
    dispatcher.start()
    trigger_thought = Thought(
        timestamp=datetime.fromtimestamp(1),
        invocation=None,
        result="An email has arrived..."
    )
    monologue = Monologue(
        id=42,
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
    db_session.add(trigger_thought)
    db_session.add(monologue)
    db_session.commit()
    
    # Assert
    # ...a fresh thread is started for new monologues
    runner.start_monologue_process.assert_called_once_with(42)


def test_dispatcher_instructs_runner_to_process_existing_unfinished_monologues(db_session, runner, dispatcher, owner):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived...",
        interval=600
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
        # allowed_actions=[]
    )
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True,
        monologues=[]
    )
    action_repo = ActionRepository(
        name="Default",
        url="some_url"
    )
    trigger_thought = Thought(
        timestamp=datetime.fromtimestamp(1),
        invocation=None,
        result="An email has arrived..."
    )
    think_action = Action(
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring="",
        repository=action_repo
    )
    verbatim_invocation = Invocation(
        action=think_action,
        function_name="think",
        params={
            "content": "I should notify the user of the new email"
        }
    )
    verbatim_thought = Thought(
        timestamp=datetime.fromtimestamp(2),
        invocation=verbatim_invocation,
        result="I should notify the user of the new email"
    )
    monologue = Monologue(
        id=45,
        title="Handle incoming email",
        summary="Thinking",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[
            trigger_thought,
            verbatim_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(trigger)
    db_session.add(event)
    db_session.add(trigger_thought)
    db_session.add(verbatim_invocation)
    db_session.add(verbatim_thought)
    db_session.add(monologue)
    db_session.commit()
    
    # Act
    dispatcher.start()
        
    # Assert
    runner.start_monologue_process.assert_called_once_with(45)

def test_dispatcher_instructs_runner_to_process_monologue_just_added_by_new_event(db_session, runner, dispatcher, owner):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived: (content)",
        interval=600
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
    )
    db_session.add(trigger)
    db_session.add(agent)
    db_session.commit()

    # Act
    dispatcher.start()
    event = Event( 
        id=42, 
        content="An email has arrived: Hello, this is...", 
        trigger=trigger, 
        dispatched=False, 
        monologues=[]
    )
    db_session.add(event)
    db_session.commit()
    dispatcher.stop()
    
    # Assert
    assert event.dispatched
    assert len(event.monologues) == 1
    runner.start_monologue_process.assert_called_once_with(event.monologues[0].id)
        
def test_dispatcher_does_nothing_for_finished_monologues(db_session, runner, dispatcher, owner):
    # Arrange
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived...",
        interval=600
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger]
        # allowed_actions=[]
    )
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True,
        monologues=[]
    )
    action_repo = ActionRepository(
        name="Default",
        url="lol.com"
    )
    trigger_thought = Thought(
        timestamp=datetime.fromtimestamp(2),
        invocation=None,
        result="An email has arrived..."
    )
    success_action = Action(
        function_name="mark_as_success",
        function_param_schema={},
        function_source_code="",
        function_docstring="",
        repository=action_repo
    )
    success_invocation = Invocation(
        action=success_action,
        function_name="mark_as_success",
        params={
            "reason": "The user has been notified"
        }   
    )
    success_thought = Thought(
        timestamp=datetime.fromtimestamp(2),
        invocation=success_invocation,
        result="I should notify the user of the new email"
    )
    monologue = Monologue(
        title="Handle incoming email",
        summary="Thinking",
        status=MonologueStatus.SUCCESS,
        agent=agent,
        thoughts=[
            trigger_thought,
            success_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(trigger)
    db_session.add(event)
    db_session.add(trigger_thought)
    db_session.add(success_invocation)
    db_session.add(success_invocation)
    db_session.add(monologue)
    db_session.commit()

    # Act
    dispatcher.start()
    
    # Assert
    runner.start_monologue_process.assert_not_called()
