import pytest
from app.services.chat import ChatExchangeCreatedEvent
from app.model.chat_exchange import ChatExchange
from app.model.chat_message import ChatMessageMarkdown
from app.model.user import User
from app.model.monologue import Monologue
from app.model.event import Event
from datetime import datetime, UTC


@pytest.mark.timeout(2)
def test_websocket_chat_exchanges_initial_listing(mock_ws, chat_mock, event_bus_mock):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()
    chat_mock.get_user_chat_exchanges_after.return_value = [
        ChatExchange(
            id=2,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1000),
            user_message=ChatMessageMarkdown(
                id=1,
                timestamp=datetime.fromtimestamp(1000),
                sending_user=User(username="John"),
                sending_agent=None,
                markdown="Hello?",
            ),
            triggered_chat_events=[
                Event(monologues=[Monologue(id=1), Monologue(id=2)]),
                Event(monologues=[Monologue(id=3)]),
            ],
        ),
        ChatExchange(
            id=3,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1200),
            user_message=None,
            triggered_chat_events=[Event(monologues=[Monologue(id=3)])],
        ),
    ]

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {"type": "chat_exchanges", "chatId": 3, "sendInitial": True},
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    res = mock_ws.receive_json()

    # Assert
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "initial",
            "exchanges": [
                {
                    "id": 2,
                    "chatId": 4,
                    "timestamp": 1000,
                    "userMessage": {
                        "id": 1,
                        "senderName": "John",
                        "timestamp": 1000,
                        "content": {"type": "markdown", "markdownText": "Hello?"},
                    },
                    "monologueIds": [1, 2, 3],
                },
                {
                    "id": 3,
                    "chatId": 4,
                    "timestamp": 1200,
                    "userMessage": None,
                    "monologueIds": [3],
                },
            ],
        },
    }


@pytest.mark.timeout(2)
def test_websocket_chat_exchanges_new_event(mock_ws, event_bus_mock, chat_mock, user):
    # Arrange
    def handler(_):
        pass

    def subscribe(t, h):
        nonlocal handler
        assert t is ChatExchangeCreatedEvent
        handler = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    chat_mock.get_user_chat_exchanges_after.return_value = [
        ChatExchange(
            id=2,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1000),
            user_message=ChatMessageMarkdown(
                id=1,
                timestamp=datetime.fromtimestamp(1000),
                sending_user=User(username="John"),
                sending_agent=None,
                markdown="Hello?",
            ),
            triggered_chat_events=[
                Event(monologues=[Monologue(id=1), Monologue(id=2)]),
                Event(monologues=[Monologue(id=3)]),
            ],
        ),
        ChatExchange(
            id=3,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1200),
            user_message=None,
            triggered_chat_events=[Event(monologues=[Monologue(id=3)])],
        ),
    ]
    chat_mock.get_user_chat_exchange.return_value = ChatExchange(
        id=3,
        chat_id=4,
        timestamp=datetime.fromtimestamp(1200),
        user_message=None,
        triggered_chat_events=[Event(monologues=[Monologue(id=3)])],
    )

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {"type": "chat_exchanges", "chatId": 3, "sendInitial": False},
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    event = ChatExchangeCreatedEvent(user_id=user.id, chat_id=3, exchange_id=3)
    handler(event)

    res = mock_ws.receive_json()

    # Assert
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "new",
            "exchange": {
                "id": 3,
                "chatId": 4,
                "timestamp": 1200,
                "userMessage": None,
                "monologueIds": [3],
            },
        },
    }


@pytest.mark.timeout(2)
def test_websocket_chat_exchanges_complex(mock_ws, event_bus_mock, chat_mock, user):
    # Arrange
    def handler(_):
        pass

    def subscribe(t, h):
        nonlocal handler
        assert t is ChatExchangeCreatedEvent
        handler = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    chat_mock.get_user_chat_exchanges_after.return_value = [
        ChatExchange(
            id=2,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1000),
            user_message=ChatMessageMarkdown(
                id=1,
                timestamp=datetime.fromtimestamp(1000),
                sending_user=user,
                sending_agent=None,
                markdown="Hello?",
            ),
            triggered_chat_events=[
                Event(monologues=[Monologue(id=1), Monologue(id=2)]),
                Event(monologues=[Monologue(id=3)]),
            ],
        ),
        ChatExchange(
            id=3,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1200),
            user_message=ChatMessageMarkdown(
                id=2,
                timestamp=datetime.fromtimestamp(1800),
                sending_user=user,
                sending_agent=None,
                markdown="Goodbye.",
            ),
            triggered_chat_events=[Event(monologues=[Monologue(id=3)])],
        ),
    ]
    chat_mock.get_user_chat_exchange.return_value = ChatExchange(
        id=5,
        chat_id=4,
        timestamp=datetime.fromtimestamp(1200),
        user_message=None,
        triggered_chat_events=[Event(monologues=[Monologue(id=3)])],
    )

    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {"type": "chat_exchanges", "chatId": 3, "sendInitial": True},
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # Sub response

    res_initial = mock_ws.receive_json()

    event = ChatExchangeCreatedEvent(user_id=user.id, chat_id=3, exchange_id=3)
    handler(event)

    res_new = mock_ws.receive_json()

    # Assert
    assert res_initial == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "initial",
            "exchanges": [
                {
                    "id": 2,
                    "chatId": 4,
                    "timestamp": 1000,
                    "userMessage": {
                        "id": 1,
                        "senderName": "John",
                        "timestamp": 1000,
                        "content": {"type": "markdown", "markdownText": "Hello?"},
                    },
                    "monologueIds": [1, 2, 3],
                },
                {
                    "id": 3,
                    "chatId": 4,
                    "timestamp": 1200,
                    "userMessage": {
                        "id": 2,
                        "senderName": "John",
                        "timestamp": 1800,
                        "content": {"type": "markdown", "markdownText": "Goodbye."},
                    },
                    "monologueIds": [3],
                },
            ],
        },
    }
    assert res_new == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "new",
            "exchange": {
                "id": 5,
                "chatId": 4,
                "timestamp": 1200,
                "userMessage": None,
                "monologueIds": [3],
            },
        },
    }
