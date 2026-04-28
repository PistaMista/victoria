import pytest
from unittest import mock
from app.services.monologues import (
    MonologueThoughtAppendedEvent,
    MonologueMetadataSetEvent,
    MonologueStatusChangedEvent,
    MonologueStatus,
)
from app.model.thought import Thought
from app.model.action import Action
from app.model.invocation import Invocation
from app.model.monologue import Monologue
from datetime import datetime
from datetime import UTC
from starlette.concurrency import run_in_threadpool
import asyncio
import gc


@pytest.fixture(scope="function")
def thought():
    action = Action(
        id=10,
        function_name="mega_func",
        function_param_schema={},
        function_source_code="",
        function_docstring="",
    )
    invocation = Invocation(
        id=20,
        action=action,
        function_name="mega_func",
        params={"the_mega_param": "foobar"},
    )
    monologue = Monologue(id=2, event_id=22)
    thought = Thought(
        id=30,
        timestamp=datetime.fromtimestamp(50, tz=UTC),
        invocation=invocation,
        monologue=monologue,
        result="Suboptimal",
    )
    return thought


@pytest.fixture(scope="function")
def thought2():
    action = Action(
        id=11,
        function_name="mega_func",
        function_param_schema={},
        function_source_code="",
        function_docstring="",
    )
    invocation = Invocation(
        id=21,
        action=action,
        function_name="mega_func",
        params={"the_mega_param": "foobar"},
    )
    monologue = Monologue(id=3, event_id=42)
    thought = Thought(
        id=31,
        timestamp=datetime.fromtimestamp(50, tz=UTC),
        invocation=invocation,
        monologue=monologue,
        result="DIFFERENT",
    )
    return thought


@pytest.mark.timeout(2)
def test_websocket_can_subscribe_when_handler_id_free(mock_ws, event_bus_mock):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()

    # Act
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 12,
        "subscription": {"type": "chat_exchanges", "chatId": 20, "sendInitial": False},
    }
    mock_ws.send_json(sub_req)
    sub_res = mock_ws.receive_json()

    # Assert
    assert sub_res == {
        "type": "subscribeResponse",
        "handlerId": 12,
        "success": True,
        "reason": "",
    }


@pytest.mark.timeout(2)
def test_websocket_can_subscribe_to_multiple_events(mock_ws, event_bus_mock):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()

    # Act
    sub_req_exchanges = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {"type": "chat_exchanges", "chatId": 20, "sendInitial": False},
    }
    sub_req_thoughts = {
        "type": "subscribeRequest",
        "handlerId": 2,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 88,
            "sendInitial": False,
        },
    }

    mock_ws.send_json(sub_req_exchanges)
    sub_res1 = mock_ws.receive_json()

    mock_ws.send_json(sub_req_thoughts)
    sub_res2 = mock_ws.receive_json()

    # Assert
    assert sub_res1 == {
        "type": "subscribeResponse",
        "handlerId": 1,
        "success": True,
        "reason": "",
    }
    assert sub_res2 == {
        "type": "subscribeResponse",
        "handlerId": 2,
        "success": True,
        "reason": "",
    }


@pytest.mark.timeout(2)
def test_websocket_cannot_subscribe_when_handler_id_taken_by_same_event_type(
    mock_ws, event_bus_mock
):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()

    # Act
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 12,
        "subscription": {"type": "chat_exchanges", "chatId": 20, "sendInitial": False},
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # First response

    mock_ws.send_json(sub_req)
    sub_res = mock_ws.receive_json()

    # Assert
    assert sub_res == {
        "type": "subscribeResponse",
        "handlerId": 12,
        "success": False,
        "reason": "handler with id 12 is already subscribed",
    }


@pytest.mark.timeout(2)
def test_websocket_cannot_subscribe_when_handler_id_taken_by_different_event_type(
    mock_ws, event_bus_mock
):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()

    # Act
    sub_req_exchanges = {
        "type": "subscribeRequest",
        "handlerId": 67,
        "subscription": {"type": "chat_exchanges", "chatId": 20, "sendInitial": False},
    }
    sub_req_thoughts = {
        "type": "subscribeRequest",
        "handlerId": 67,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 88,
            "sendInitial": False,
        },
    }

    mock_ws.send_json(sub_req_exchanges)
    mock_ws.receive_json()  # First response

    mock_ws.send_json(sub_req_thoughts)
    sub_res = mock_ws.receive_json()

    # Assert
    assert sub_res == {
        "type": "subscribeResponse",
        "handlerId": 67,
        "success": False,
        "reason": "handler with id 67 is already subscribed",
    }


@pytest.mark.timeout(2)
def test_websocket_can_unsubscribe_when_handler_subscribed(mock_ws, event_bus_mock):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()

    # Act
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 67,
        "subscription": {"type": "chat_exchanges", "chatId": 20, "sendInitial": False},
    }
    unsub_req = {
        "type": "unsubscribeRequest",
        "handlerId": 67,
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # First response

    mock_ws.send_json(unsub_req)
    unsub_res = mock_ws.receive_json()

    # Assert
    assert unsub_res == {
        "type": "unsubscribeResponse",
        "handlerId": 67,
        "success": True,
        "reason": "",
    }


@pytest.mark.timeout(2)
def test_websocket_cannot_unsubscribe_when_handler_not_subscribed(
    mock_ws, event_bus_mock
):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()

    # Act
    unsub_req = {
        "type": "unsubscribeRequest",
        "handlerId": 67,
    }

    mock_ws.send_json(unsub_req)
    unsub_res = mock_ws.receive_json()

    # Assert
    assert unsub_res == {
        "type": "unsubscribeResponse",
        "handlerId": 67,
        "success": False,
        "reason": "handler with id 67 is not subscribed",
    }


@pytest.mark.timeout(2)
def test_websocket_cannot_unsubscribe_twice(mock_ws, event_bus_mock):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()

    # Act
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 67,
        "subscription": {"type": "chat_exchanges", "chatId": 20, "sendInitial": False},
    }
    unsub_req = {
        "type": "unsubscribeRequest",
        "handlerId": 67,
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    mock_ws.send_json(unsub_req)
    mock_ws.receive_json()  # First unsub response

    mock_ws.send_json(unsub_req)
    unsub_res = mock_ws.receive_json()

    # Assert
    assert unsub_res == {
        "type": "unsubscribeResponse",
        "handlerId": 67,
        "success": False,
        "reason": "handler with id 67 is not subscribed",
    }


@pytest.mark.timeout(2)
def test_websocket_forwards_subscribed_event_from_event_bus(
    mock_ws, event_bus_mock, user, thought
):
    # Arrange
    handlers = []

    def subscribe(t, h):
        nonlocal handlers
        assert t is MonologueThoughtAppendedEvent
        handlers.append(h)
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 20,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 88,
            "sendInitial": False,
        },
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    # Act
    event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=88, thought=thought
    )
    for handler in handlers:
        handler(event)
    res = mock_ws.receive_json()

    # Assert
    assert res["type"] == "eventMessage"
    assert res["handlerIds"] == [20]


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_websocket_filters_events_from_event_bus_based_on_owner_id(
    mock_ws, event_bus_mock, user, thought, thought2
):
    # Arrange
    handlers = []

    def subscribe(t, h):
        nonlocal handlers
        assert t is MonologueThoughtAppendedEvent
        handlers.append(h)
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 20,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 88,
            "sendInitial": False,
        },
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    # Act
    thought_event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=88, thought=thought2
    )

    thought_event_foreign = MonologueThoughtAppendedEvent(
        user_id=user.id + 40, monologue_id=88, thought=thought
    )
    for handler in handlers:
        handler(thought_event)
        handler(thought_event_foreign)

    res = mock_ws.receive_json()

    # Assert
    assert res["type"] == "eventMessage"
    assert res["handlerIds"] == [20]
    assert res["content"]["thought"]["result"] == "DIFFERENT"

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(run_in_threadpool(mock_ws.receive_text), 1.0)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_websocket_filters_events_from_event_bus_based_on_object_id(
    mock_ws, event_bus_mock, user, thought, thought2
):
    # Arrange
    handlers = []

    def subscribe(t, h):
        nonlocal handlers
        assert t is MonologueThoughtAppendedEvent
        handlers.append(h)
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 20,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 1,
            "sendInitial": False,
        },
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    # Act
    thought_event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=1, thought=thought
    )

    thought_event_foreign = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=2, thought=thought2
    )
    for handler in handlers:
        handler(thought_event)
        handler(thought_event_foreign)

    res = mock_ws.receive_json()

    # Assert
    assert res["type"] == "eventMessage"
    assert res["handlerIds"] == [20]
    assert res["content"]["thought"]["result"] == "Suboptimal"

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(run_in_threadpool(mock_ws.receive_text), 1.0)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_websocket_groups_events_for_same_object_subscriptions(
    mock_ws, event_bus_mock, user, thought
):
    # Arrange
    handlers = []

    def subscribe(t, h):
        nonlocal handlers
        assert t is MonologueThoughtAppendedEvent
        handlers.append(h)
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe

    sub_req_1 = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 1,
            "sendInitial": False,
        },
    }
    sub_req_2 = {
        "type": "subscribeRequest",
        "handlerId": 21,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 1,
            "sendInitial": False,
        },
    }

    mock_ws.send_json(sub_req_1)
    mock_ws.receive_json()  # Sub response 1
    mock_ws.send_json(sub_req_2)
    mock_ws.receive_json()  # Sub response 2

    # Act
    thought_event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=1, thought=thought
    )

    for handler in handlers:
        handler(thought_event)

    res = mock_ws.receive_json()

    # Assert
    assert res["type"] == "eventMessage"
    assert res["handlerIds"] == [1, 21]

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(run_in_threadpool(mock_ws.receive_text), 1.0)


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_websocket_no_longer_forwards_events_from_event_bus_after_unsubscribe(
    mock_ws, event_bus_mock, user, thought
):
    # Arrange
    handlers = []

    def subscribe(t, h):
        nonlocal handlers
        assert t is MonologueThoughtAppendedEvent
        handlers.append(h)

        def unsub():
            handlers.remove(h)

        return unsub

    event_bus_mock.subscribe.side_effect = subscribe

    # Act
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 67,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 1,
            "sendInitial": False,
        },
    }
    unsub_req = {
        "type": "unsubscribeRequest",
        "handlerId": 67,
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    mock_ws.send_json(unsub_req)
    mock_ws.receive_json()  # Unsub response

    thought_event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=1, thought=thought
    )

    for handler in handlers:
        handler(thought_event)

    # Assert
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(run_in_threadpool(mock_ws.receive_text), 1.0)
    assert not handlers


@pytest.mark.timeout(2)
def test_websocket_not_groups_events_for_two_same_object_subscriptions_after_one_unsubscribes(
    mock_ws, event_bus_mock, user, thought
):
    # Arrange
    handlers = []

    def subscribe(t, h):
        nonlocal handlers
        assert t is MonologueThoughtAppendedEvent
        handlers.append(h)
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe

    sub_req_1 = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 1,
            "sendInitial": False,
        },
    }
    sub_req_2 = {
        "type": "subscribeRequest",
        "handlerId": 21,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 1,
            "sendInitial": False,
        },
    }
    unsub_req_1 = {
        "type": "unsubscribeRequest",
        "handlerId": 1,
    }

    mock_ws.send_json(sub_req_1)
    mock_ws.receive_json()  # Sub response 1
    mock_ws.send_json(sub_req_2)
    mock_ws.receive_json()  # Sub response 2

    # Act
    mock_ws.send_json(unsub_req_1)
    mock_ws.receive_json()  # Unsub response

    thought_event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=1, thought=thought
    )

    for handler in handlers:
        handler(thought_event)

    res = mock_ws.receive_json()

    # Assert
    assert res["type"] == "eventMessage"
    assert res["handlerIds"] == [21]


@pytest.mark.timeout(2)
def test_websocket_unsubscribes_from_event_bus_after_disconnect(
    mock_ws, event_bus_mock
):
    # Arrange
    unsub = mock.MagicMock()
    event_bus_mock.subscribe.return_value = unsub

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 67,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": 1,
            "sendInitial": False,
        },
    }

    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    # Act
    mock_ws.close()
    gc.collect()

    # Assert
    unsub.assert_called_once()
