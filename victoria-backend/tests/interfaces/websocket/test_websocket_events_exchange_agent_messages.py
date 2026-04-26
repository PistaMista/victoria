import pytest
from app.services.chat import ChatMessageSentEvent
from app.model.chat_message import (
    ChatMessageMarkdown,
    ChatMessageChoicePrompt,
    ChoiceMessageOption,
)
from app.model.agent import Agent
from app.model.user import User
from datetime import datetime
from starlette.concurrency import run_in_threadpool
import asyncio


@pytest.mark.timeout(2)
def test_websocket_exchange_agent_messages_initial_listing(
    mock_ws, event_bus_mock, chat_mock, user
):
    # Arrange
    event_bus_mock.subscribe.return_value = lambda: ()
    chat_mock.get_user_exchange_replies_after.return_value = [
        ChatMessageMarkdown(
            id=1,
            timestamp=datetime.fromtimestamp(1000),
            sending_user=User(username="John"),
            sending_agent=None,
            markdown="Hello!",
        ),
        ChatMessageChoicePrompt(
            id=2,
            timestamp=datetime.fromtimestamp(1100),
            sending_user=None,
            sending_agent=Agent(name="Cook"),
            prompt="Pick an option",
            choices=[
                ChoiceMessageOption(value="lol"),
                ChoiceMessageOption(value="woo"),
            ],
        ),
    ]
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "exchange_agent_messages",
            "exchangeId": 12,
            "sendInitial": True,
        },
    }

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # sub response

    res = mock_ws.receive_json()

    # Assert
    chat_mock.get_user_exchange_replies_after.assert_called_with(
        user_id=user.id, exchange_id=12, after=0
    )
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "initial",
            "messages": [
                {
                    "id": 1,
                    "timestamp": 1000,
                    "senderName": "John",
                    "content": {"type": "markdown", "markdownText": "Hello!"},
                },
                {
                    "id": 2,
                    "timestamp": 1100,
                    "senderName": "Cook",
                    "content": {
                        "type": "choice_prompt",
                        "prompt": "Pick an option",
                        "queryId": 2,
                        "choices": [{"value": "lol"}, {"value": "woo"}],
                    },
                },
            ],
        },
    }


@pytest.mark.timeout(2)
def test_websocket_exchange_agent_messages_new_event(
    mock_ws, event_bus_mock, chat_mock, user
):
    # Arrange
    def handler(_):
        pass

    def subscribe(t, h):
        nonlocal handler
        assert t is ChatMessageSentEvent
        handler = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    chat_mock.get_user_chat_message.return_value = ChatMessageMarkdown(
        id=10,
        timestamp=datetime.fromtimestamp(1500),
        sending_user=None,
        sending_agent=Agent(name="Arthas"),
        markdown="Welcome to Azeroth",
    )
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "exchange_agent_messages",
            "exchangeId": 12,
            "sendInitial": False,
        },
    }
    event = ChatMessageSentEvent(
        user_id=user.id, chat_id=1, exchange_id=12, reply_id=10
    )

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # sub response

    handler(event)
    res = mock_ws.receive_json()

    chat_mock.get_user_chat_message.assert_called_with(user_id=user.id, message_id=10)
    assert res == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "new",
            "message": {
                "id": 10,
                "timestamp": 1500,
                "senderName": "Arthas",
                "content": {"type": "markdown", "markdownText": "Welcome to Azeroth"},
            },
        },
    }


@pytest.mark.timeout(2)
@pytest.mark.asyncio
async def test_websocket_exchange_agent_messages_handler_does_not_react_to_user_messages(
    mock_ws, event_bus_mock, chat_mock, user
):
    # Arrange
    def handler(_):
        pass

    def subscribe(t, h):
        nonlocal handler
        assert t is ChatMessageSentEvent
        handler = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    chat_mock.get_user_chat_message.return_value = ChatMessageMarkdown(
        id=10,
        timestamp=datetime.fromtimestamp(1500),
        sending_user=None,
        sending_agent=Agent(name="Arthas"),
        markdown="Welcome to Azeroth",
    )
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "exchange_agent_messages",
            "exchangeId": 12,
            "sendInitial": False,
        },
    }
    event = ChatMessageSentEvent(
        user_id=user.id, chat_id=1, exchange_id=100, reply_id=None
    )

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # sub response

    handler(event)

    # Assert
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(run_in_threadpool(mock_ws.receive_text), 1.0)


@pytest.mark.timeout(2)
def test_websocket_exchange_agent_messages_complex(
    mock_ws, event_bus_mock, chat_mock, user
):
    # Arrange
    def handler(_):
        pass

    def subscribe(t, h):
        nonlocal handler
        assert t is ChatMessageSentEvent
        handler = h
        return lambda: ()

    event_bus_mock.subscribe.side_effect = subscribe
    chat_mock.get_user_exchange_replies_after.return_value = [
        ChatMessageMarkdown(
            id=1,
            timestamp=datetime.fromtimestamp(1000),
            sending_user=User(username="John"),
            sending_agent=None,
            markdown="Hello!",
        ),
        ChatMessageChoicePrompt(
            id=2,
            timestamp=datetime.fromtimestamp(1100),
            sending_user=None,
            sending_agent=Agent(name="Cook"),
            prompt="Pick an option",
            choices=[
                ChoiceMessageOption(value="lol"),
                ChoiceMessageOption(value="woo"),
            ],
        ),
    ]
    chat_mock.get_user_chat_message.return_value = ChatMessageMarkdown(
        id=10,
        timestamp=datetime.fromtimestamp(1500),
        sending_user=None,
        sending_agent=Agent(name="Arthas"),
        markdown="Welcome to Azeroth",
    )
    sub_req = {
        "type": "subscribeRequest",
        "handlerId": 1,
        "subscription": {
            "type": "exchange_agent_messages",
            "exchangeId": 12,
            "sendInitial": True,
        },
    }
    new_event = ChatMessageSentEvent(
        user_id=user.id, chat_id=1, exchange_id=12, reply_id=10
    )

    # Act
    mock_ws.send_json(sub_req)
    mock_ws.receive_json()  # sub response

    res_initial = mock_ws.receive_json()

    handler(new_event)
    res_new = mock_ws.receive_json()

    # Assert
    assert res_initial == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "initial",
            "messages": [
                {
                    "id": 1,
                    "timestamp": 1000,
                    "senderName": "John",
                    "content": {"type": "markdown", "markdownText": "Hello!"},
                },
                {
                    "id": 2,
                    "timestamp": 1100,
                    "senderName": "Cook",
                    "content": {
                        "type": "choice_prompt",
                        "prompt": "Pick an option",
                        "queryId": 2,
                        "choices": [{"value": "lol"}, {"value": "woo"}],
                    },
                },
            ],
        },
    }
    assert res_new == {
        "type": "eventMessage",
        "handlerIds": [1],
        "content": {
            "type": "new",
            "message": {
                "id": 10,
                "timestamp": 1500,
                "senderName": "Arthas",
                "content": {"type": "markdown", "markdownText": "Welcome to Azeroth"},
            },
        },
    }
