import pytest
from unittest import mock
import threading
from typing import Callable
from app.services.monologues import MonologueStatusChangedEvent
from app.services.monologues.runner import RunnerService, AlreadyRunningError
from app.services.monologues.runner.monologue_thread import MonologueThread
from app.services.db import DatabaseService
from app.model.user import User, Role
from app.model.agent import Agent
from app.model.event import Event
from app.model.monologue import Monologue, MonologueStatus
from app.model.thought import Thought
from app.model.invocation import Invocation
from app.model.trigger import PollTrigger
from datetime import datetime


@pytest.fixture(scope="function")
def owner():
    return User(id=42, username="John", password_hash="", role=Role.USER)


@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)

    with mock.patch.object(db, "get_session_factory", return_value=db_factory):
        yield db


def test_runner_starts_new_thread_for_running_monologues(
    db_serv, db_session, owner, event_bus_mock
):
    # Arrange
    mock_thread = mock.MagicMock()
    thread_factory = mock.MagicMock(side_effect=[mock_thread])

    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=1,
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    trigger_thought = Thought(
        timestamp=datetime.now(),
        invocation=None,
        result="News entry added: A cure for cancer discovered...",
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[trigger_thought],
    )
    event.monologues = [monologue]

    db_session.add(monologue)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)

    # Assert
    thread_factory.assert_called_once_with(7, runner.on_thread_exited)
    mock_thread.start.assert_called_once()


def test_runner_marks_running_monologues_as_running(
    db_serv, db_session, owner, event_bus_mock
):
    # Arrange
    mock_thread = mock.MagicMock()
    thread_factory = mock.MagicMock(side_effect=[mock_thread])

    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=1,
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    trigger_thought = Thought(
        timestamp=datetime.now(),
        invocation=None,
        result="News entry added: A cure for cancer discovered...",
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[trigger_thought],
    )
    event.monologues = [monologue]

    db_session.add(monologue)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)

    # Assert
    assert monologue.status == MonologueStatus.RUNNING
    event_bus_mock.publish.assert_called_with(
        MonologueStatusChangedEvent(
            user_id=42, monologue_id=7, status=MonologueStatus.RUNNING
        )
    )


def test_runner_marks_queued_monologues_as_pending(
    db_serv, db_session, owner, event_bus_mock
):
    # Arrange
    mock_thread = mock.MagicMock()
    thread_factory = mock.MagicMock(side_effect=[mock_thread])

    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=0,
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    trigger_thought = Thought(
        timestamp=datetime.now(),
        invocation=None,
        result="News entry added: A cure for cancer discovered...",
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        # lets say the server crashed while the monologue was running
        status=MonologueStatus.RUNNING,
        thoughts=[trigger_thought],
    )
    event.monologues = [monologue]

    db_session.add(monologue)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)

    # Assert
    assert monologue.status == MonologueStatus.PENDING
    event_bus_mock.publish.assert_called_with(
        MonologueStatusChangedEvent(
            user_id=42, monologue_id=7, status=MonologueStatus.PENDING
        )
    )


def test_runner_ignores_finished_monologues(db_serv, db_session, owner, event_bus_mock):
    # Arrange
    mock_thread1 = mock.MagicMock()
    mock_thread2 = mock.MagicMock()
    thread_factory = mock.MagicMock(side_effect=[mock_thread1, mock_thread2])

    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=10000,
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    success = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.SUCCESS,
        thoughts=[],
    )
    failure = Monologue(
        id=8,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.FAILURE,
        thoughts=[],
    )
    event.monologues = [success, failure]

    db_session.add(success)
    db_session.add(failure)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)
    runner.start_monologue_process(8)

    # Assert
    assert success.status == MonologueStatus.SUCCESS
    assert failure.status == MonologueStatus.FAILURE

    thread_factory.assert_not_called()
    mock_thread1.start.assert_not_called()
    mock_thread2.start.assert_not_called()

    event_bus_mock.publish.assert_not_called()


def test_runner_cannot_start_running_monologue(
    db_serv, db_session, owner, event_bus_mock
):
    # Arrange
    mock_thread = mock.MagicMock()
    mock_thread._id = 7
    thread_factory = mock.MagicMock(side_effect=[mock_thread])

    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=1,
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    trigger_thought = Thought(
        timestamp=datetime.now(),
        invocation=None,
        result="News entry added: A cure for cancer discovered...",
    )
    monologue = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[trigger_thought],
    )
    event.monologues = [monologue]

    db_session.add(monologue)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)

    with pytest.raises(AlreadyRunningError):
        runner.start_monologue_process(7)

    # Assert
    thread_factory.assert_called_once_with(7, runner.on_thread_exited)
    assert monologue.status == MonologueStatus.RUNNING


def test_runner_queues_excess_monologues(db_serv, db_session, owner, event_bus_mock):
    # Arrange
    mock_thread1 = mock.MagicMock()
    mock_thread2 = mock.MagicMock()
    thread_factory = mock.MagicMock(side_effect=[mock_thread1, mock_thread2])

    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=1,
    )
    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    mon1 = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[],
    )
    mon2 = Monologue(
        id=8,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[],
    )
    event.monologues = [mon1, mon2]

    db_session.add(mon1)
    db_session.add(mon2)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)
    runner.start_monologue_process(8)

    # Assert
    mock_thread1.start.assert_called_once()
    mock_thread2.start.assert_not_called()

    assert mon1.status == MonologueStatus.RUNNING
    assert mon2.status == MonologueStatus.PENDING

    event_bus_mock.publish.assert_any_call(
        MonologueStatusChangedEvent(
            user_id=42, monologue_id=7, status=MonologueStatus.RUNNING
        )
    )
    event_bus_mock.publish.assert_any_call(
        MonologueStatusChangedEvent(
            user_id=42, monologue_id=8, status=MonologueStatus.PENDING
        )
    )


def test_runner_starts_first_queued_thread_after_a_thread_finishes(
    db_serv, db_session, owner, event_bus_mock
):
    # Arrange
    thread_factory = mock.MagicMock()
    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=1,
    )

    class MockThread(MonologueThread):
        def __init__(
            self,
            id: int,
            wait_event: threading.Event,
            on_finish: Callable[[MonologueThread], None],
        ):
            super().__init__(id, on_finish=on_finish)
            self._event = wait_event
            self._mock = mock.MagicMock()

        def start(self):
            super().start()
            self._mock.start()

        def run(self):
            self._event.wait()
            self._mock.run()
            self._on_finish(self)

    event1 = threading.Event()
    event2 = threading.Event()

    mock_thread1 = MockThread(7, event1, runner.on_thread_exited)
    mock_thread2 = MockThread(8, event2, runner.on_thread_exited)
    thread_factory.side_effect = [mock_thread1, mock_thread2]

    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    mon1 = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[],
    )
    mon2 = Monologue(
        id=8,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[],
    )
    event.monologues = [mon1, mon2]

    db_session.add(mon1)
    db_session.add(mon2)
    db_session.commit()

    # Act / Assert
    try:
        runner.start_monologue_process(7)
        runner.start_monologue_process(8)

        mock_thread1._mock.start.assert_called_once()
        mock_thread2._mock.start.assert_not_called()

        assert event_bus_mock.publish.call_count == 2
        event_bus_mock.publish.assert_any_call(
            MonologueStatusChangedEvent(
                user_id=42, monologue_id=7, status=MonologueStatus.RUNNING
            )
        )
        event_bus_mock.publish.assert_any_call(
            MonologueStatusChangedEvent(
                user_id=42, monologue_id=8, status=MonologueStatus.PENDING
            )
        )
        event_bus_mock.reset_mock()

        event1.set()
        mock_thread1.join()

        assert mon1.is_finished()

        mock_thread1._mock.start.assert_called_once()
        mock_thread2._mock.start.assert_called_once()

        assert event_bus_mock.publish.call_count == 2
        event_bus_mock.publish.assert_any_call(
            MonologueStatusChangedEvent(
                user_id=42, monologue_id=7, status=MonologueStatus.FAILURE
            )
        )
        event_bus_mock.publish.assert_any_call(
            MonologueStatusChangedEvent(
                user_id=42, monologue_id=8, status=MonologueStatus.RUNNING
            )
        )

        assert mon2.status == MonologueStatus.RUNNING

        event2.set()
        mock_thread2.join()
    finally:
        event1.set()
        event2.set()

        mock_thread1.join()
        mock_thread2.join()


def test_runner_marks_prematurely_exited_threads_as_failed_monologues(
    db_serv, db_session, owner, event_bus_mock
):
    # Arrange
    thread_factory = mock.MagicMock()
    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=1,
    )

    class MockThread(MonologueThread):
        def __init__(
            self,
            id: int,
            wait_event: threading.Event,
            on_finish: Callable[[MonologueThread], None],
        ):
            super().__init__(id, on_finish)
            self._mock = mock.MagicMock()
            self._event = wait_event

        def start(self):
            super().start()
            self._mock.start()

        def run(self):
            self._event.wait()
            self._mock.run()
            self._on_finish(self)

    event1 = threading.Event()
    mock_thread1 = MockThread(7, event1, runner.on_thread_exited)
    thread_factory.side_effect = [mock_thread1]

    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    mon1 = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[],
    )
    event.monologues = [mon1]

    db_session.add(mon1)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)
    event1.set()  # ...exit the thread
    mock_thread1.join()

    # ...threads that end without being marked as success are considered failed
    assert mon1.status == MonologueStatus.FAILURE
    assert event_bus_mock.publish.call_count == 2
    event_bus_mock.publish.assert_called_with(
        MonologueStatusChangedEvent(
            user_id=42, monologue_id=7, status=MonologueStatus.FAILURE
        )
    )


def test_runner_does_not_mark_exited_threads_as_failed_monologues_if_already_marked(
    db_serv, db_session, owner, event_bus_mock
):
    # Arrange
    thread_factory = mock.MagicMock()
    runner = RunnerService(
        db_service=db_serv,
        event_bus_service=event_bus_mock,
        thread_factory=thread_factory,
        thread_limit=100000,
    )

    class MockThread(MonologueThread):
        def __init__(
            self,
            id: int,
            wait_event: threading.Event,
            on_finish: Callable[[MonologueThread], None],
        ):
            super().__init__(id, on_finish)
            self._mock = mock.MagicMock()
            self._event = wait_event

        def start(self):
            super().start()
            self._mock.start()

        def run(self):
            self._event.wait()
            self._mock.run()
            self._on_finish(self)

    event1 = threading.Event()
    event2 = threading.Event()

    mock_thread1 = MockThread(7, event1, runner.on_thread_exited)
    mock_thread2 = MockThread(8, event2, runner.on_thread_exited)
    thread_factory.side_effect = [mock_thread1, mock_thread2]

    trigger = PollTrigger(
        name="Trigger",
        url="http://seznam.cz",
        template="News entry added: (content)",
        interval=1200,
    )
    agent = Agent(
        name="Reporter",
        prompt="Notify the user of important world news",
        owner=owner,
        allowed_triggers=[trigger],
    )
    event = Event(
        content="News entry added: A cure for cancer discovered...",
        trigger=trigger,
        dispatched=True,
        monologues=[],
    )
    mon1 = Monologue(
        id=7,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[],
    )
    mon2 = Monologue(
        id=8,
        title="None",
        summary="None",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        thoughts=[],
    )
    event.monologues = [mon1, mon2]

    db_session.add(mon1)
    db_session.add(mon2)
    db_session.commit()

    # Act
    runner.start_monologue_process(7)
    runner.start_monologue_process(8)

    mon1.status = MonologueStatus.SUCCESS
    mon2.status = MonologueStatus.FAILURE
    db_session.commit()

    event1.set()  # ...exit the threads
    event2.set()  # ...exit the threads

    mock_thread1.join()
    mock_thread2.join()

    # Assert
    assert mon1.status == MonologueStatus.SUCCESS
    assert mon2.status == MonologueStatus.FAILURE


# TODO: Make the runner handle threads that crash and do not call on_finish - the AgenticMonologueThread as a try-catch block, but it would be
# better to have the runner handle it.
