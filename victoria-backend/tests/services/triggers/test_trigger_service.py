import pytest
import time
from unittest import mock
from sqlalchemy import select, func
from app.services.trigger import TriggerService, TriggerDiff, WebhookTriggerDiff, ChatTriggerDiff, PollTriggerDiff, TimerTriggerDiff, NonexistentTriggerError, NonexistentEventError
from app.services.db import DatabaseService
from app.model.event import Event
from app.model.user import User, Role
from app.model.trigger import Trigger, TimerTrigger, PollTrigger, WebhookTrigger, ChatTrigger

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db



def test_trigger_service_can_get_user_event(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    user = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(poll_trigger)
    db_session.add(user)
    db_session.add(event)
    db_session.commit()

    # Act
    res = serv.get_user_event(
        user_id=10,
        event_id=3
    )

    # Assert
    assert res.content == "Wooo"
    assert res.trigger.id == 5
    assert not res.dispatched

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_get_all_registered_triggers(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    webhook_trigger = WebhookTrigger(
        id=15,
        name="WEBHOOKAH",
        endpoint="wooo",
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, webhook_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act
    res = serv.get_all_triggers()

    # Assert
    assert len(res) == 3
    assert isinstance(res[0], PollTrigger)
    assert res[0].id == 5
    assert isinstance(res[1], ChatTrigger)
    assert res[1].id == 10
    assert isinstance(res[2], WebhookTrigger)
    assert res[2].id == 15

    # Teardown
    serv.stop_trigger_timers()


def test_trigger_service_can_get_user_allowed_triggers(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    webhook_trigger = WebhookTrigger(
        id=15,
        name="WEBHOOKAH",
        endpoint="wooo",
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, webhook_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act
    res = serv.get_user_allowed_triggers(
        user_id=10
    )

    # Assert
    assert len(res) == 2
    assert isinstance(res[0], PollTrigger)
    assert res[0].id == 5
    assert isinstance(res[1], WebhookTrigger)
    assert res[1].id == 15

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_returns_empty_list_for_allowed_triggers_of_nonexistent_user(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    webhook_trigger = WebhookTrigger(
        id=15,
        name="WEBHOOKAH",
        endpoint="wooo",
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, webhook_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act
    res = serv.get_user_allowed_triggers(
        user_id=99
    )

    # Assert
    assert res == []

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_get_trigger_by_id(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    webhook_trigger = WebhookTrigger(
        id=15,
        name="WEBHOOKAH",
        endpoint="wooo",
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, webhook_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act
    res = serv.get_trigger_by_id(id=10)

    # Assert
    assert isinstance(res, ChatTrigger)
    assert res.id == 10
    assert res.name == "Simple chat"
    assert res.receiver == "general"
    assert res.template == "Hello"

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_add_webhook_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(poll_trigger)
    db_session.add(event)
    db_session.commit()

    # Act
    new_id = serv.add_webhook_trigger(
        name="Sha'ggoth the Devourer of Celestial Planes",
        template="TEMPLATE",
        endpoint="/woo"
    )

    # Assert
    new_trigger = db_session.scalar(
        select(Trigger).where(Trigger.id == new_id)
    )
    trigger_count = db_session.scalar(
        select(func.count()).select_from(Trigger)
    )

    assert trigger_count == 2
    assert isinstance(new_trigger, WebhookTrigger)
    assert new_trigger.name == "Sha'ggoth the Devourer of Celestial Planes"
    assert new_trigger.template == "TEMPLATE"
    assert new_trigger.endpoint == "/woo"

    # Teardown
    serv.stop_trigger_timers()


def test_trigger_service_can_add_chat_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(poll_trigger)
    db_session.add(event)
    db_session.commit()

    # Act
    new_id = serv.add_chat_trigger(
        name="CHAT",
        template="Temp",
        receiver="iseeyou"
    )

    # Assert
    new_trigger = db_session.scalar(
        select(Trigger).where(Trigger.id == new_id)
    )
    trigger_count = db_session.scalar(
        select(func.count()).select_from(Trigger)
    )

    assert trigger_count == 2
    assert isinstance(new_trigger, ChatTrigger)
    assert new_trigger.name == "CHAT"
    assert new_trigger.template == "Temp"
    assert new_trigger.receiver == "iseeyou"

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_add_timer_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(poll_trigger)
    db_session.add(event)
    db_session.commit()

    # Act
    new_id = serv.add_timer_trigger(
        name="tajmr",
        template="Tajmr templejt",
        interval=2000
    )

    # Assert
    new_trigger = db_session.scalar(
        select(Trigger).where(Trigger.id == new_id)
    )
    trigger_count = db_session.scalar(
        select(func.count()).select_from(Trigger)
    )

    assert trigger_count == 2
    assert isinstance(new_trigger, TimerTrigger)
    assert new_trigger.name == "tajmr"
    assert new_trigger.template == "Tajmr templejt"
    assert new_trigger.interval == 2000

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_add_poll_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(poll_trigger)
    db_session.add(event)
    db_session.commit()

    # Act
    new_id = serv.add_poll_trigger(
        name="tajmr",
        template="Tajmr templejt",
        interval=2000,
        url="seznam.cz"
    )

    # Assert
    new_trigger = db_session.scalar(
        select(Trigger).where(Trigger.id == new_id)
    )
    trigger_count = db_session.scalar(
        select(func.count()).select_from(Trigger)
    )

    assert trigger_count == 2
    assert isinstance(new_trigger, PollTrigger)
    assert new_trigger.name == "tajmr"
    assert new_trigger.template == "Tajmr templejt"
    assert new_trigger.interval == 2000
    assert new_trigger.url == "seznam.cz"

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.restart_trigger_timer")
def test_trigger_service_tries_to_start_trigger_timer_when_timer_trigger_added(mock_restart, db_serv):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )

    # Act
    mock_restart.reset_mock()
    new_id = serv.add_timer_trigger(
        name="tajmr",
        template="Tajmr templejt",
        interval=2000
    )

    # Assert
    mock_restart.assert_called_with(trigger_id=new_id)

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.restart_trigger_timer")
def test_trigger_service_tries_to_start_trigger_timer_when_poll_trigger_added(mock_restart, db_serv):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )

    # Act
    mock_restart.reset_mock()
    new_id = serv.add_poll_trigger(
        name="tajmr",
        template="Tajmr templejt",
        interval=2000,
        url="google.com"
    )

    # Assert
    mock_restart.assert_called_with(trigger_id=new_id)

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_update_base_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = ChatTrigger(
        id=5,
        name="Linux Talk",
        receiver="technical",
        template="Old"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=TriggerDiff(
            name="Windows Talk"
        )
    )

    # Assert
    db_session.refresh(trigger)
    assert trigger.name == "Windows Talk"
    assert trigger.template == "Old"
    assert trigger.receiver == "technical"

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_update_webhook_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = WebhookTrigger(
        id=5,
        name="Original",
        endpoint="/pringles",
        template="SALTIER THAN SALT"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=WebhookTriggerDiff(
            template="Not salty anymore",
            endpoint="/woo?"
        )
    )

    # Assert
    db_session.refresh(trigger)
    assert trigger.name == "Original"
    assert trigger.template == "Not salty anymore"
    assert trigger.endpoint == "/woo?"

    # Teardown
    serv.stop_trigger_timers()


def test_trigger_service_can_update_chat_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = ChatTrigger(
        id=5,
        name="Advice",
        receiver="advisory",
        template="Woo"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=ChatTriggerDiff(
            receiver="lol"
        )
    )

    # Assert
    db_session.refresh(trigger)
    assert trigger.name == "Advice"
    assert trigger.template == "Woo"
    assert trigger.receiver == "lol"

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_update_timer_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = TimerTrigger(
        id=5,
        name="Check logs",
        interval=120,
        template="Check the logs"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=TimerTriggerDiff(
            name="Czech",
            interval=20
        )
    )

    # Assert
    db_session.refresh(trigger)
    assert trigger.name == "Czech"
    assert trigger.template == "Check the logs"
    assert trigger.interval == 20

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_update_poll_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = PollTrigger(
        id=5,
        name="Check news",
        template="Download news articles",
        interval=120,
        url="novinky.cz"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=PollTriggerDiff(
            template="mm",
            url="woo.com"
        )
    )

    # Assert
    db_session.refresh(trigger)
    assert trigger.name == "Check news"
    assert trigger.template == "mm"
    assert trigger.interval == 120
    assert trigger.url == "woo.com"

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_update_trigger_type_and_convert_chat_trigger_to_poll_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = ChatTrigger(
        id=5,
        name="Advice",
        receiver="advisory",
        template="Woo"
    )
    event = Event(
        trigger=trigger, # Foreign key constraint must not break during trigger type change
        dispatched=False,
        content=""
    )
    db_session.add(event)
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=PollTriggerDiff(
            name="Download advice",
            url="seznam.cz"
        )
    )

    # Assert
    db_session.expunge(trigger)
    trigger = db_session.scalar(
        select(Trigger).where(Trigger.id == 5)
    )

    assert isinstance(trigger, PollTrigger)
    assert trigger.name == "Download advice"
    assert trigger.template == "Woo"
    # When unspecified, the default interval is one hour
    assert trigger.interval == 3600
    assert trigger.url == "seznam.cz"

    # Relationships must not be broken
    assert isinstance(event.trigger, PollTrigger)
    assert event.trigger.id == 5

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.restart_trigger_timer")
def test_trigger_service_tries_to_restart_timer_when_updating_timer_trigger(mock_restart, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = TimerTrigger(
        id=5,
        name="Check logs",
        interval=120,
        template="Check the logs"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=TimerTriggerDiff(
            name="Czech",
            interval=20
        )
    )

    # Assert
    mock_restart.assert_called_with(trigger_id=5)

    # Teardown
    serv.stop_trigger_timers()


@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.restart_trigger_timer")
def test_trigger_service_tries_to_restart_timer_when_updating_poll_trigger(mock_restart, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = PollTrigger(
        id=5,
        name="Check logs",
        interval=120,
        template="Check the logs",
        url="novinky.cz"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=PollTriggerDiff(
            name="Czech",
            interval=20
        )
    )

    # Assert
    mock_restart.assert_called_with(trigger_id=5)

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.restart_trigger_timer")
def test_trigger_service_tries_to_restart_timer_when_changing_chat_trigger_to_timer_trigger(mock_restart, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = ChatTrigger(
        id=5,
        name="Advice",
        receiver="advisory",
        template="Woo"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=PollTriggerDiff(
            name="Czech",
            interval=20,
            url="novinky.cz"
        )
    )

    # Assert
    mock_restart.assert_called_with(trigger_id=5)

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.restart_trigger_timer")
def test_trigger_service_tries_to_restart_timer_when_changing_webhook_trigger_to_poll_trigger(mock_restart, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = WebhookTrigger(
        id=5,
        name="Original",
        endpoint="/pringles",
        template="SALTIER THAN SALT"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=PollTriggerDiff(
            name="Czech",
            interval=20,
            url="novinky.cz"
        )
    )

    # Assert
    mock_restart.assert_called_with(trigger_id=5)

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.restart_trigger_timer")
def test_trigger_service_tries_to_restart_timer_when_changing_timer_trigger_to_poll_trigger(mock_restart, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    trigger = TimerTrigger(
        id=5,
        name="Check logs",
        interval=120,
        template="Check the logs"
    )
    db_session.add(trigger)
    db_session.commit()

    # Act
    serv.update_trigger(
        trigger_id=5,
        changes=PollTriggerDiff(
            name="Czech",
            interval=20,
            url="novinky.cz"
        )
    )

    # Assert
    mock_restart.assert_called_with(trigger_id=5)

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_remove_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    timer_trigger = TimerTrigger(
        id=15,
        name="WEBHOOKAH",
        interval=40,
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, timer_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act
    serv.remove_trigger(id=10)

    # Assert
    triggers = db_session.scalars(
        select(Trigger)
    ).all()

    assert len(triggers) == 2
    assert triggers[0].id == 5
    assert triggers[1].id == 15

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.stop_trigger_timer")
def test_trigger_service_removing_timer_trigger_tries_to_stop_trigger_timer(mock_stop, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    timer_trigger = TimerTrigger(
        id=15,
        name="WEBHOOKAH",
        interval=40,
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, timer_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act
    serv.remove_trigger(id=15)

    # Assert
    mock_stop.assert_called_once_with(trigger_id=15)

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.stop_trigger_timer")
def test_trigger_service_removing_poll_trigger_tries_to_stop_trigger_timer(mock_stop, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    timer_trigger = TimerTrigger(
        id=15,
        name="WEBHOOKAH",
        interval=40,
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, timer_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act
    serv.remove_trigger(id=5)

    # Assert
    mock_stop.assert_called_once_with(trigger_id=5)

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.start_stopped_trigger_timers")
def test_trigger_service_tries_to_start_stopped_trigger_timers_on_startup(mock_start_timers, db_serv):
    # Arrange

    # Act 
    serv = TriggerService(
        database_service=db_serv
    )

    # Assert
    mock_start_timers.assert_called_once()

    # Teardown
    serv.stop_trigger_timers()



def test_trigger_service_can_generate_simple_event_from_given_trigger_id_and_variables(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    db_session.add(poll_trigger)
    db_session.commit()

    # Act
    event_id = serv.generate_event(5, {
        "content": "Hello!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
    assert events[0].id == event_id
    assert events[0].trigger_id == 5
    assert events[0].content == "Content of the website: Hello!"
    assert not events[0].dispatched

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_generate_complex_event_from_given_trigger_id_and_variables(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = ChatTrigger(
        id=5,
        name="General chat",
        template="New event - new user chat message in chat ID $(chat_id). The message is: $(msg_content).",
        receiver="general"
    )
    db_session.add(poll_trigger)
    db_session.commit()

    # Act
    event_id = serv.generate_event(5, {
        "chat_id": "92530",
        "msg_content": "MORE CHEESE!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
    assert events[0].id == event_id
    assert events[0].trigger_id == 5
    assert events[0].content == "New event - new user chat message in chat ID 92530. The message is: MORE CHEESE!."
    assert not events[0].dispatched

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_generate_event_from_given_trigger_id_and_variables_when_variable_in_template_undefined(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = ChatTrigger(
        id=5,
        name="General chat",
        template="New event - new user chat message in chat ID $(chat_id). The message is: $(msg_content).",
        receiver="general"
    )
    db_session.add(poll_trigger)
    db_session.commit()

    # Act
    event_id = serv.generate_event(5, {
        # chat_id is not defined
        "msg_content": "MORE CHEESE!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
    assert events[0].id == event_id
    assert events[0].trigger_id == 5
    assert events[0].content == "New event - new user chat message in chat ID . The message is: MORE CHEESE!."
    assert not events[0].dispatched

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_can_generate_event_from_given_trigger_id_and_variables_when_variable_in_template_not_string(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = ChatTrigger(
        id=5,
        name="General chat",
        template="New event - new user chat message in chat ID $(chat_id). The message is: $(msg_content).",
        receiver="general"
    )
    db_session.add(poll_trigger)
    db_session.commit()

    # Act
    event_id = serv.generate_event(5, {
        "chat_id": 404,
        "msg_content": "MORE CHEESE!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
    assert events[0].id == event_id
    assert events[0].trigger_id == 5
    assert events[0].content == "New event - new user chat message in chat ID 404. The message is: MORE CHEESE!."
    assert not events[0].dispatched

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_throws_when_trying_to_generate_event_with_invalid_trigger_id(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = ChatTrigger(
        id=5,
        name="General chat",
        template="",
        receiver="general"
    )
    db_session.add(poll_trigger)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentTriggerError):
        serv.generate_event(999999999999, {
            "chat_id": 404,
            "msg_content": "MORE CHEESE!"
        })

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_timer_trigger_generates_events_periodically(mock_generate, db_serv, db_session):
    # Arrange
    timer_trigger = TimerTrigger(
        id=42,
        name="Timer",
        template="Event!",
        interval=1
    )
    db_session.add(timer_trigger)
    db_session.commit()

    # Act
    serv = TriggerService(
        database_service=db_serv
    )

    # Assert
    time.sleep(1.5)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {})

    time.sleep(1.0)
    assert mock_generate.call_count == 2
    mock_generate.assert_called_with(42, {})

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_timer_trigger_does_not_start_multiple_times(mock_generate, db_serv, db_session):
    # Arrange
    timer_trigger = TimerTrigger(
        id=42,
        name="Timer",
        template="Event!",
        interval=1
    )
    db_session.add(timer_trigger)
    db_session.commit()

    # Act
    serv = TriggerService(
        database_service=db_serv
    )

    serv.start_stopped_trigger_timers()
    serv.start_stopped_trigger_timers()
    serv.start_stopped_trigger_timers()

    # Assert
    time.sleep(1.5)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {})

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_timer_trigger_can_be_started_after_being_added(mock_generate, db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )

    # Act
    timer_trigger = TimerTrigger(
        id=42,
        name="Timer",
        template="Event!",
        interval=1
    )
    db_session.add(timer_trigger)
    db_session.commit()

    serv.start_stopped_trigger_timers()

    # Assert
    time.sleep(1.5)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {})

    # Teardown
    serv.stop_trigger_timers()


@mock.patch("app.services.trigger.requests.get")
@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_poll_trigger_polls_website_periodically(mock_generate, mock_get, db_serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=42,
        name="Poll",
        template="Website: $(content) $(lol)",
        url="http://seznam.cz",
        interval=1
    )
    db_session.add(poll_trigger)
    db_session.commit()

    mock_res = mock_get.return_value
    mock_res.status_code = 200
    mock_res.text = "Content!"

    # Act
    serv = TriggerService(
        database_service=db_serv
    )

    # Assert
    time.sleep(1.5)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {"content": "Content!"})

    mock_res.text = "New"
    time.sleep(1.0)
    assert mock_generate.call_count == 2
    mock_generate.assert_called_with(42, {"content": "New"})

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_can_restart_specific_trigger_timer(mock_generate, db_serv, db_session):
    # Arrange
    timer_trigger = TimerTrigger(
        id=42,
        name="Timer",
        template="Event!",
        interval=1
    )
    db_session.add(timer_trigger)
    db_session.commit()

    serv = TriggerService(
        database_service=db_serv
    )

    # Act / Assert
    time.sleep(1.5)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {})

    time.sleep(0.6)
    assert mock_generate.call_count == 2
    mock_generate.assert_called_with(42, {})

    serv.restart_trigger_timer(trigger_id=42)
    time.sleep(0.8)
    assert mock_generate.call_count == 2

    serv.restart_trigger_timer(trigger_id=42)
    time.sleep(0.8)
    assert mock_generate.call_count == 2

    time.sleep(0.8)
    assert mock_generate.call_count == 3
    mock_generate.assert_called_with(42, {})

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_can_stop_specific_trigger_timer(mock_generate, db_serv, db_session):
    # Arrange
    timer_trigger = TimerTrigger(
        id=42,
        name="Timer",
        template="Event!",
        interval=1
    )
    db_session.add(timer_trigger)
    db_session.commit()

    serv = TriggerService(
        database_service=db_serv
    )

    # Act / Assert
    time.sleep(1.5)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {})

    serv.stop_trigger_timer(trigger_id=42)

    time.sleep(1.0)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {})

    time.sleep(1.0)
    assert mock_generate.call_count == 1
    mock_generate.assert_called_with(42, {})

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_chat_trigger_receives_chat_message_and_generates_chat_events(mock_generate, db_serv, db_session):
    # Arrange
    chat_trigger_1 = ChatTrigger(
        id=1,
        name="Chat 1",
        template="New message from user: $(message)",
        receiver="general"
    )
    chat_trigger_2 = ChatTrigger(
        id=2,
        name="Chat 2",
        template="NEW TASK GIVEN: $(message)",
        receiver="general"
    )
    db_session.add(chat_trigger_1)
    db_session.add(chat_trigger_2)
    db_session.commit()
    
    serv = TriggerService(
        database_service=db_serv
    )

    # Act
    mock_generate.side_effect = lambda id, _: {
        1: 30,
        2: 40
    }.get(id)
    res_hello = serv.receive_chat_message(
        receiver="general", 
        message="Hello there",
        chat_id=40,
        exchange_id=None
    )
    mock_generate.side_effect = lambda id, _: {
        1: 99,
        2: 100
    }.get(id)
    res_goodbye = serv.receive_chat_message(
        receiver="general", 
        message="Goodbye",
        chat_id=50,
        exchange_id=20
    )

    # Assert
    mock_generate.assert_any_call(1, {"message": "Hello there", "chatId": 40, "exchangeId": None})
    mock_generate.assert_any_call(2, {"message": "Hello there", "chatId": 40, "exchangeId": None})
    mock_generate.assert_any_call(1, {"message": "Goodbye", "chatId": 50, "exchangeId": 20})
    mock_generate.assert_any_call(2, {"message": "Goodbye", "chatId": 50, "exchangeId": 20})

    assert res_hello == [30, 40]
    assert res_goodbye == [99, 100]

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_chat_trigger_generates_chat_events_only_for_messages_matching_chat_receiver(mock_generate, db_serv, db_session):
    # Arrange
    chat_trigger_1 = ChatTrigger(
        id=1,
        name="Chat 1",
        template="New message from user: $(message)",
        receiver="general"
    )
    chat_trigger_2 = ChatTrigger(
        id=2,
        name="Chat 2",
        template="NEW TASK GIVEN: $(message)",
        receiver="technical"
    )
    db_session.add(chat_trigger_1)
    db_session.add(chat_trigger_2)
    db_session.commit()
    
    serv = TriggerService(
        database_service=db_serv
    )
    mock_generate.side_effect = lambda id, _: {
        1: 99,
        2: 100
    }.get(id)

    # Act
    res_hello = serv.receive_chat_message("general", "Hello there")
    res_goodbye = serv.receive_chat_message("general", "Goodbye")

    # Assert
    assert mock_generate.call_count == 2
    mock_generate.assert_any_call(1, {"message": "Hello there", "chatId": None, "exchangeId": None})
    mock_generate.assert_any_call(1, {"message": "Goodbye", "chatId": None, "exchangeId": None})
    assert res_hello == [99]
    assert res_goodbye == [99]

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_webhook_trigger_receives_webhook_payload_and_generates_events(mock_generate, db_serv, db_session):
    # Arrange
    webhook_trigger_1 = WebhookTrigger(
        id=1,
        name="Webhook",
        template="Incoming HTTP request: $(payload)",
        endpoint="/test/modify"
    )
    webhook_trigger_2 = WebhookTrigger(
        id=2,
        name="Webhook",
        template="REQUEST: $(payload)",
        endpoint="/test/modify"
    )
    db_session.add(webhook_trigger_1)
    db_session.add(webhook_trigger_2)
    db_session.commit()

    serv = TriggerService(
        database_service=db_serv
    )

    # Act
    serv.receive_webhook_payload("/test/modify", "load")
    serv.receive_webhook_payload("/test/modify", "foobar")

    # Assert
    mock_generate.assert_any_call(1, {"payload": "load"})
    mock_generate.assert_any_call(1, {"payload": "foobar"})
    mock_generate.assert_any_call(2, {"payload": "load"})
    mock_generate.assert_any_call(2, {"payload": "foobar"})

    # Teardown
    serv.stop_trigger_timers()

@mock.patch("tests.services.triggers.test_trigger_service.TriggerService.generate_event")
def test_trigger_service_webhook_trigger_generates_events_only_for_payloads_matching_endpoint(mock_generate, db_serv, db_session):
    # Arrange
    webhook_trigger_1 = WebhookTrigger(
        id=1,
        name="Webhook",
        template="Incoming HTTP request: $(payload)",
        endpoint="/test/modify"
    )
    webhook_trigger_2 = WebhookTrigger(
        id=2,
        name="Webhook",
        template="REQUEST: $(payload)",
        endpoint="/test/create"
    )
    db_session.add(webhook_trigger_1)
    db_session.add(webhook_trigger_2)
    db_session.commit()

    serv = TriggerService(
        database_service=db_serv
    )

    # Act
    serv.receive_webhook_payload("/test/modify", "load")
    serv.receive_webhook_payload("/test/modify", "foobar")

    # Assert
    assert mock_generate.call_count == 2
    mock_generate.assert_any_call(1, {"payload": "load"})
    mock_generate.assert_any_call(1, {"payload": "foobar"})

    # Teardown
    serv.stop_trigger_timers()

def test_trigger_service_throws_when_manipulating_nonexistent_trigger(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    webhook_trigger = WebhookTrigger(
        id=15,
        name="WEBHOOKAH",
        endpoint="wooo",
        template="Lol"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger, webhook_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentTriggerError):
        serv.get_trigger_by_id(id=99)

    with pytest.raises(NonexistentTriggerError):
        serv.restart_trigger_timer(trigger_id=99)

    with pytest.raises(NonexistentTriggerError):
        serv.stop_trigger_timer(trigger_id=99)

    with pytest.raises(NonexistentTriggerError):
        serv.update_trigger(trigger_id=99, changes=TriggerDiff())

    with pytest.raises(NonexistentTriggerError):
        serv.remove_trigger(id=99)

    # Teardown
    serv.stop_trigger_timers()


def test_trigger_service_throws_when_manipulating_nonexistent_event(db_serv, db_session):
    # Arrange
    serv = TriggerService(
        database_service=db_serv
    )
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        template="wooo",
        receiver="general"
    )
    user_allowed = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[poll_trigger]
    )
    user_not_allowed = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger]
    )
    event = Event(
        id=3,
        trigger=poll_trigger,
        content="Wooo",
        dispatched=False
    )
    db_session.add(poll_trigger)
    db_session.add(user_allowed)
    db_session.add(user_not_allowed)
    db_session.add(event)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentEventError):
        serv.get_user_event(
            user_id=99, # Nonexistent
            event_id=3
        )

    with pytest.raises(NonexistentEventError):
        serv.get_user_event(
            user_id=10,
            event_id=4 # Nonexistent
        )

    with pytest.raises(NonexistentEventError):
        serv.get_user_event(
            user_id=20, # Does not allow poll_trigger
            event_id=3
        )

    # Teardown
    serv.stop_trigger_timers()
