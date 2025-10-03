import pytest
import time
from unittest import mock
from sqlalchemy import select
from app.services.trigger import TriggerService, NonexistentTriggerError
from app.services.db import DatabaseService
from app.model.event import Event
from app.model.trigger import TimerTrigger, PollTrigger, WebhookTrigger, ChatTrigger

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

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
    serv.generate_event(5, {
        "content": "Hello!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
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
    serv.generate_event(5, {
        "chat_id": "92530",
        "msg_content": "MORE CHEESE!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
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
    serv.generate_event(5, {
        # chat_id is not defined
        "msg_content": "MORE CHEESE!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
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
    serv.generate_event(5, {
        "chat_id": 404,
        "msg_content": "MORE CHEESE!"
    })

    # Assert
    events = db_session.scalars(
        select(Event)
    ).all()

    assert len(events) == 1
    assert events[0].trigger_id == 5
    assert events[0].content == "New event - new user chat message in chat ID 404. The message is: MORE CHEESE!."
    assert not events[0].dispatched

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
    serv.receive_chat_message("general", "Hello there")
    serv.receive_chat_message("general", "Goodbye")

    # Assert
    mock_generate.assert_any_call(1, {"message": "Hello there"})
    mock_generate.assert_any_call(2, {"message": "Hello there"})
    mock_generate.assert_any_call(1, {"message": "Goodbye"})
    mock_generate.assert_any_call(2, {"message": "Goodbye"})

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

    # Act
    serv.receive_chat_message("general", "Hello there")
    serv.receive_chat_message("general", "Goodbye")

    # Assert
    assert mock_generate.call_count == 2
    mock_generate.assert_any_call(1, {"message": "Hello there"})
    mock_generate.assert_any_call(1, {"message": "Goodbye"})

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
