import pytest
from app.services.monologues import MonologueThoughtAppendedEvent
from app.model.user import User
from app.model.monologue import Monologue, MonologueStatus
from app.model.thought import Thought
from app.model.invocation import Invocation
from app.model.agent import Agent
from app.model.event import Event
from datetime import datetime, UTC


@pytest.mark.timeout(2)
def test_websocket_monologue_thoughts_initial_listing(
    mock_ws, event_bus_mock, monologue_mock, user
):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()
    monologue = Monologue(
        id=1337,
        status=MonologueStatus.PENDING,
        agent=Agent(id=600),
        event_id=33,
        event=Event(id=33),
    )
    monologue_mock.get_user_monologue_thoughts.return_value = [
        Thought(
            id=1,
            timestamp=datetime.fromtimestamp(1),
            monologue=monologue,
            invocation=None,
            result="An email has arrived...",
        ),
        Thought(
            id=2,
            timestamp=datetime.fromtimestamp(2),
            monologue=monologue,
            invocation=Invocation(
                function_name="think",
                params={"content": "I should add it to the calendar"},
            ),
            result="I should add it to the calendar",
        ),
        Thought(
            id=3,
            timestamp=datetime.fromtimestamp(3),
            monologue=monologue,
            invocation=Invocation(
                function_name="add_to_calendar",
                params={"event_name": "Conference", "event_timestamp": 20000},
            ),
            result="Event successfully added to calendar",
        ),
        Thought(
            id=4,
            timestamp=datetime.fromtimestamp(4),
            monologue=monologue,
            invocation=Invocation(
                function_name="end_monologue",
                params={"successful": True, "reason": "Email processed"},
            ),
        ),
        Thought(
            id=5,
            timestamp=datetime.fromtimestamp(5),
            monologue=monologue,
            invocation=Invocation(
                function_name="end_monologue",
                params={"successful": False, "reason": "Email processing failed"},
            ),
        ),
    ]

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": monologue.id,
            "sendInitial": True,
        },
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    res = mock_ws.receive_json()

    # Assert
    monologue_mock.get_user_monologue_thoughts.assert_called_with(
        user_id=user.id, monologue_id=monologue.id
    )
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "initial",
            "thoughts": [
                {
                    "id": 1,
                    "startTimestamp": 1,
                    "invocation": {
                        "type": "TriggerInvocation",
                        "name": None,
                        "parameters": {"eventId": 33},
                    },
                    "result": "An email has arrived...",
                },
                {
                    "id": 2,
                    "startTimestamp": 2,
                    "invocation": {
                        "type": "ThoughtInvocation",
                        "name": None,
                        "parameters": {"thought": "I should add it to the calendar"},
                    },
                    "result": "I should add it to the calendar",
                },
                {
                    "id": 3,
                    "startTimestamp": 3,
                    "invocation": {
                        "type": "ActionInvocation",
                        "name": "add_to_calendar",
                        "parameters": {
                            "event_name": "Conference",
                            "event_timestamp": 20000,
                        },
                    },
                    "result": "Event successfully added to calendar",
                },
                {
                    "id": 4,
                    "startTimestamp": 4,
                    "invocation": {
                        "type": "SuccessInvocation",
                        "name": None,
                        "parameters": {},
                    },
                    "result": "",
                },
                {
                    "id": 5,
                    "startTimestamp": 5,
                    "invocation": {
                        "type": "FailureInvocation",
                        "name": None,
                        "parameters": {},
                    },
                    "result": "",
                },
            ],
        },
    }


@pytest.mark.timeout(2)
def test_websocket_monologue_thoughts_new_event(mock_ws, event_bus_mock, user):
    # Arrange
    def handler(_):
        pass

    def subscribe(t, h):
        nonlocal handler
        assert t is MonologueThoughtAppendedEvent
        handler = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    monologue = Monologue(
        id=1337,
        status=MonologueStatus.PENDING,
        agent=Agent(id=600),
        event_id=33,
        event=Event(id=33),
    )
    thought = Thought(
        id=40,
        timestamp=datetime.fromtimestamp(300),
        monologue=monologue,
        invocation=Invocation(
            function_name="trigger_ha_entity",
            params={"entity_name": "lock_front_door:unlock"},
        ),
        result="Device triggered successfully",
    )
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": monologue.id,
            "sendInitial": False,
        },
    }
    event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=monologue.id, thought=thought
    )

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    handler(event)
    res = mock_ws.receive_json()

    # Assert
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "new",
            "thought": {
                "id": 40,
                "startTimestamp": 300,
                "invocation": {
                    "type": "ActionInvocation",
                    "name": "trigger_ha_entity",
                    "parameters": {"entity_name": "lock_front_door:unlock"},
                },
                "result": "Device triggered successfully",
            },
        },
    }


@pytest.mark.timeout(2)
def test_websocket_monologue_thoughts_complex(
    mock_ws, event_bus_mock, monologue_mock, user
):
    # Arrange
    def handler(_):
        pass

    def subscribe(t, h):
        nonlocal handler
        assert t is MonologueThoughtAppendedEvent
        handler = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    monologue = Monologue(
        id=1337,
        status=MonologueStatus.PENDING,
        agent=Agent(id=600),
        event_id=33,
        event=Event(id=33),
    )
    monologue_mock.get_user_monologue_thoughts.return_value = [
        Thought(
            id=1,
            timestamp=datetime.fromtimestamp(1),
            monologue=monologue,
            invocation=None,
            result="An email has arrived...",
        ),
        Thought(
            id=2,
            timestamp=datetime.fromtimestamp(2),
            monologue=monologue,
            invocation=Invocation(
                function_name="think",
                params={"content": "I should add it to the calendar"},
            ),
            result="I should add it to the calendar",
        ),
    ]
    new_thought = Thought(
        id=40,
        timestamp=datetime.fromtimestamp(300),
        monologue=monologue,
        invocation=Invocation(
            function_name="trigger_ha_entity",
            params={"entity_name": "lock_front_door:unlock"},
        ),
        result="Device triggered successfully",
    )
    append_event = MonologueThoughtAppendedEvent(
        user_id=user.id, monologue_id=monologue.id, thought=new_thought
    )

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "monologue_thoughts",
            "monologueId": monologue.id,
            "sendInitial": True,
        },
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    initial_res = mock_ws.receive_json()

    handler(append_event)
    new_res = mock_ws.receive_json()

    # Assert
    monologue_mock.get_user_monologue_thoughts.assert_called_with(
        user_id=user.id, monologue_id=monologue.id
    )
    assert initial_res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "initial",
            "thoughts": [
                {
                    "id": 1,
                    "startTimestamp": 1,
                    "invocation": {
                        "type": "TriggerInvocation",
                        "name": None,
                        "parameters": {"eventId": 33},
                    },
                    "result": "An email has arrived...",
                },
                {
                    "id": 2,
                    "startTimestamp": 2,
                    "invocation": {
                        "type": "ThoughtInvocation",
                        "name": None,
                        "parameters": {"thought": "I should add it to the calendar"},
                    },
                    "result": "I should add it to the calendar",
                },
            ],
        },
    }
    assert new_res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "new",
            "thought": {
                "id": 40,
                "startTimestamp": 300,
                "invocation": {
                    "type": "ActionInvocation",
                    "name": "trigger_ha_entity",
                    "parameters": {"entity_name": "lock_front_door:unlock"},
                },
                "result": "Device triggered successfully",
            },
        },
    }
