import pytest
from app.model.monologue import Monologue, MonologueStatus
from app.services.monologues import (
    MonologueMetadataSetEvent,
    MonologueStatusChangedEvent,
)
from datetime import datetime, UTC


@pytest.fixture(scope="function")
def monologue():
    return Monologue(
        id=1,
        title="TITLE",
        summary="SUMMARY",
        status=MonologueStatus.RUNNING,
        agent_id=42,
        dispatched_at=datetime.fromtimestamp(300, UTC),
        modified_at=datetime.fromtimestamp(400, UTC),
    )


@pytest.mark.timeout(2)
def test_websocket_monologue_status_initial(
    mock_ws, event_bus_mock, monologue_mock, monologue, user
):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()
    monologue_mock.get_user_monologue.return_value = monologue
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_status",
            "monologueId": monologue.id,
            "sendInitial": True,
        },
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # sub response

    res = mock_ws.receive_json()

    monologue_mock.get_user_monologue.assert_called_with(
        user_id=user.id, monologue_id=monologue.id
    )
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "monologue": {
                "id": 1,
                "agentId": 42,
                "startTimestamp": 300,
                "endTimestamp": 400,
                "title": "TITLE",
                "summary": "SUMMARY",
                "status": "RUNNING",
            }
        },
    }


@pytest.mark.timeout(2)
def test_websocket_monologue_status_event_fires_when_metadata_changes(
    mock_ws, event_bus_mock, monologue_mock, monologue, user
):
    # Arrange
    handlers = {}

    def subscribe(t, h):
        handlers[t] = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    monologue_mock.get_user_monologue.return_value = monologue
    event = MonologueMetadataSetEvent(
        user_id=user.id, monologue_id=monologue.id, title="TITLE", summary="SDASDKNKJN"
    )
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_status",
            "monologueId": monologue.id,
            "sendInitial": False,
        },
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # sub response

    handlers[MonologueMetadataSetEvent](event)
    res = mock_ws.receive_json()

    monologue_mock.get_user_monologue.assert_called_with(
        user_id=user.id, monologue_id=monologue.id
    )
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "monologue": {
                "id": 1,
                "agentId": 42,
                "startTimestamp": 300,
                "endTimestamp": 400,
                "title": "TITLE",
                "summary": "SUMMARY",
                "status": "RUNNING",
            }
        },
    }


@pytest.mark.timeout(2)
def test_websocket_monologue_status_event_fires_when_status_changes(
    mock_ws, event_bus_mock, monologue_mock, user, monologue
):
    # Arrange
    handlers = {}

    def subscribe(t, h):
        handlers[t] = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    monologue_mock.get_user_monologue.return_value = monologue
    event = MonologueStatusChangedEvent(
        user_id=user.id, monologue_id=monologue.id, status=MonologueStatus.RUNNING
    )
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_status",
            "monologueId": monologue.id,
            "sendInitial": False,
        },
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # sub response

    handlers[MonologueStatusChangedEvent](event)
    res = mock_ws.receive_json()

    monologue_mock.get_user_monologue.assert_called_with(
        user_id=user.id, monologue_id=monologue.id
    )
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "monologue": {
                "id": 1,
                "agentId": 42,
                "startTimestamp": 300,
                "endTimestamp": 400,
                "title": "TITLE",
                "summary": "SUMMARY",
                "status": "RUNNING",
            }
        },
    }
