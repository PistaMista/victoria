import pytest
from unittest import mock
import threading
from app.services.monologues.runner import RunnerService, MonologueThread, AlreadyRunningError
from app.services.db import DatabaseService
from app.model.agent import Agent
from app.model.event import Event
from app.model.monologue import Monologue, MonologueStatus
from app.model.thought import Thought
from app.model.invocation import TriggerInvocation, ThoughtInvocation, SuccessInvocation
from app.model.trigger import PollTrigger


@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

def test_runner_starts_new_thread_for_running_monologues(db_serv, db_session):
    # Arrange
    runner = RunnerService(
        db_service=db_serv,
        thread_limit=1
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        allowed_triggers=[trigger]
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[]
    )
    trigger_invocation = TriggerInvocation(
        event=event
    )
    trigger_thought = Thought(
        invocation=trigger_invocation,
        result="News entry added: A cure for cancer discovered..."
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[
            trigger_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(monologue)
    db_session.commit()
    
    with mock.patch("app.services.monologues.runner.MonologueThread") as MonologueThread:
        instance = MonologueThread.return_value
        instance.start.return_value = None

        # Act
        runner.start_monologue_process(7)

        # Assert
        MonologueThread.assert_called_once_with(7)
        instance.start.assert_called_once()


def test_runner_marks_running_monologues_as_running(db_serv, db_session):
    # Arrange
    runner = RunnerService(
        db_service=db_serv,
        thread_limit=1
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        allowed_triggers=[trigger]
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[]
    )
    trigger_invocation = TriggerInvocation(
        event=event
    )
    trigger_thought = Thought(
        invocation=trigger_invocation,
        result="News entry added: A cure for cancer discovered..."
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[
            trigger_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(monologue)
    db_session.commit()
    
    # Act
    runner.start_monologue_process(7)
    
    # Assert
    assert monologue.status == MonologueStatus.RUNNING
    

def test_runner_marks_queued_monologues_as_pending(db_serv, db_session):
    # Arrange
    runner = RunnerService(
        db_service=db_serv,
        thread_limit=0
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        allowed_triggers=[trigger]
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[]
    )
    trigger_invocation = TriggerInvocation(
        event=event
    )
    trigger_thought = Thought(
        invocation=trigger_invocation,
        result="News entry added: A cure for cancer discovered..."
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        # lets say the server crashed while the monologue was running
        status=MonologueStatus.RUNNING, 
        thoughts=[
            trigger_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(monologue)
    db_session.commit()
    
    # Act
    runner.start_monologue_process(7)
    
    # Assert
    assert monologue.status == MonologueStatus.PENDING    

def test_runner_ignores_finished_monologues(db_serv, db_session):
    # Arrange
    runner = RunnerService(
        db_service=db_serv,
        thread_limit=10000
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        allowed_triggers=[trigger]
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[]
    )
    success = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.SUCCESS,
        thoughts=[ ]
    )
    failure = Monologue(
        id=8,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.FAILURE,
        thoughts=[ ]
    )
    event.monologues = [ success, failure ]
    
    db_session.add(success)
    db_session.add(failure)
    db_session.commit()
    
    with mock.patch("app.services.monologues.runner.MonologueThread") as MonologueThread:
        instance = MonologueThread.return_value
        instance.start.return_value = None

        # Act
        runner.start_monologue_process(7)
        runner.start_monologue_process(8)
    
        # Assert
        assert success.status == MonologueStatus.SUCCESS    
        assert failure.status == MonologueStatus.FAILURE    
        MonologueThread.assert_not_called()
        instance.start.assert_not_called()

def test_runner_cannot_start_running_monologue(db_serv, db_session):
    # Arrange
    runner = RunnerService(
        db_service=db_serv,
        thread_limit=1
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        allowed_triggers=[trigger]
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[]
    )
    trigger_invocation = TriggerInvocation(
        event=event
    )
    trigger_thought = Thought(
        invocation=trigger_invocation,
        result="News entry added: A cure for cancer discovered..."
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[
            trigger_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(monologue)
    db_session.commit()

    with mock.patch("app.services.monologues.runner.MonologueThread") as MonologueThread:
        instance = MonologueThread.return_value
        instance._id = 7
        instance.start.return_value = None

        # Act
        runner.start_monologue_process(7)
        
        with pytest.raises(AlreadyRunningError):
            runner.start_monologue_process(7)

        # Assert
        MonologueThread.assert_called_once_with(7)
        assert monologue.status == MonologueStatus.RUNNING

def test_runner_queues_excess_monologues(db_serv, db_session):
    # Arrange
    runner = RunnerService(
        db_service=db_serv,
        thread_limit=1
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        allowed_triggers=[trigger]
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[]
    )
    mon1 = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[ ]
    )
    mon2 = Monologue(
        id=8,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[ ]
    )
    event.monologues = [ mon1, mon2 ]
    
    db_session.add(mon1)
    db_session.add(mon2)
    db_session.commit()

    with mock.patch("app.services.monologues.runner.MonologueThread") as MonologueThread:
        instance = MonologueThread.return_value
        instance.start.return_value = None

        # Act
        runner.start_monologue_process(7)
        runner.start_monologue_process(8)

        # Assert
        instance.start.assert_called_once()
        
        assert mon1.status == MonologueStatus.RUNNING
        assert mon2.status == MonologueStatus.PENDING

def test_runner_starts_first_queued_monologue_after_a_monologue_finishes(db_serv, db_session):
    # Arrange
    runner = RunnerService(
        db_service=db_serv,
        thread_limit=1
    )
    wait_event = threading.Event()
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        allowed_triggers=[trigger]
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[]
    )
    mon1 = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[ ]
    )
    mon2 = Monologue(
        id=8,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[ ]
    )
    event.monologues = [ mon1, mon2 ]
    
    db_session.add(mon1)
    db_session.add(mon2)
    db_session.commit()
    
    def mon1_thread():
        wait_event.wait()
    
    # Act
    with mock.patch("app.services.monologues.runner.MonologueThread") as MonologueThread:
        instance = MonologueThread.return_value
        instance.run.side_effect = mon1_thread
        
        runner.start_monologue_process(7)
        runner.start_monologue_process(8)

    with mock.patch("app.services.monologues.runner.MonologueThread") as MonologueThread:
        instance = MonologueThread.return_value
        instance.start.return_value = None
        
        wait_event.set()

        # Assert
        MonologueThread.assert_called_once_with(8)
        
        # ...threads that end without being marked as success are considered failed
        # TODO: Assert this fact in a separate test
        assert mon1.status == MonologueStatus.FAILURE
        assert mon2.status == MonologueStatus.RUNNING
