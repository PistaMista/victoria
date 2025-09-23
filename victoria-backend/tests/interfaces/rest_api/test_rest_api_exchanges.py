from fastapi import status
from app.model.user import User
from app.model.agent import Agent
from app.services.chat import NonexistentExchangeError
from app.services.auth import NotLoggedInError
from datetime import datetime
import time
import threading

def test_get_exchange_messages_returns_200_and_message_when_new_messages_available(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_exchange_replies.return_value = [
        MarkdownMessage(
            id=1,
            timestamp=datetime.fromtimestamp(1000),
            sending_user=User(
                username="John"
            ),
            sending_agent=None,
            markdown="Hello!"
        ),
        ChoicePromptMessage(
            id=2,
            timestamp=datetime.fromtimestamp(1100),
            sending_user=None,
            sending_agent=Agent(
                name="Cook"
            ),
            prompt="Pick an option",
            choices=[
                ChoiceOption(
                    value="lol"
                ),
                ChoiceOption(
                    value="woo"
                )
            ]
        )
    ]

    # Act
    res = mock_client.get(
        "/api/exchanges/42/messages"
    )

    # Assert
    chat_mock.get_user_exchange_replies.assert_called_with(
        user_id=1,
        exchange_id=42
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "timestamp": 1000,
            "senderName": "John",
            "content": {
                "type": "markdown",
                "markdownText": "Hello!"
            }
        },
        {
            "id": 2,
            "timestamp": 1100,
            "senderName": "Cook",
            "content": {
                "type": "choice_prompt",
                "prompt": "Pick an option",
                # Query ID is the same as the ID of the message
                "queryId": 2,
                "choices": [
                    { "value": "lol" },
                    { "value": "woo" }
                ]
            }
        }
    ]

def test_get_exchange_messages_waits_until_new_messages_available_before_returning_200_and_data(mock_client, auth_mock, chat_mock, user):
    # Arrange
    mock_client.get_as_non_admin_user.return_value = user
    chat_mock.get_user_exchange_replies.return_value = []

    def data_source():
        time.sleep(2)
        chat_mock.get_user_exchange_replies.return_value = [
            MarkdownMessage(
                id=1,
                timestamp=datetime.fromtimestamp(1000),
                sending_user=User(
                    username="John"
                ),
                sending_agent=None,
                markdown="hello"
            )
        ]
        
    source_thread = threading.Thread(target=data_source)
    source_thread.start()

    # Act
    res = mock_client.get(
        "/api/exchanges/42/messages"
    )
    source_thread.join()

    # Assert
    chat_mock.get_user_exchange_replies.assert_called_with(
        user_id=1,
        exchange_id=42
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "timestamp": 1000,
            "senderName": "John",
            "content": {
                "type": "markdown",
                "markdownText": "hello"
            }
        }
    ]

def test_get_exchange_messages_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/exchanges/42/messages"
    )

    # Assert
    chat_mock.get_user_exchange_replies.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_exchange_messages_returns_404_for_nonexistent_exchange(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_exchange_replies.side_effect = NonexistentExchangeError(20)

    # Act
    res = mock_client.get(
        "/api/exchanges/20/messages"
    )

    # Assert
    chat_mock.get_user_exchange_replies.assert_called_with(
        user_id=1,
        exchange_id=42
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_send_reply_returns_200_and_adds_markdown_message_on_agent_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.post(
        "/api/exchanges/42/send-reply",
        json={
            "type": "markdown",
            "message": "Message!",
            "from_agent_id": 33
        }
    )

    # Assert
    chat_mock.send_markdown_reply_to_user_exchange.assert_called_with(
        user_id=1,
        exchange_id=42,
        from_agent_id=33,
        markdown="Message!"
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {}

def test_send_reply_returns_200_adds_message_with_choice_prompt_and_returns_query_id_on_agent_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.send_choice_reply_to_user_exchange.return_value = 50

    # Act
    res = mock_client.post(
        "/api/exchanges/42/send-reply",
        json={
            "type": "choice",
            "prompt": "Pick a thing",
            "choices": ["choice1", 2],
            "from_agent_id": 33
        }
    )

    # Assert
    chat_mock.send_choice_reply_to_user_exchange.assert_called_with(
        user_id=1,
        exchange_id=42,
        from_agent_id=33,
        prompt="Pick a thing",
        choices=["choice1", 2]
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json == {
        "queryId": 50
    }

def test_send_reply_returns_400_when_unknown_message_type_specified(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.post(
        "/api/exchanges/42/send-reply",
        json={
            "type": "lol",
            "prompt": "Pick a thing",
            "choices": ["choice1", 2],
            "from_agent_id": 33
        }
    )

    # Assert
    chat_mock.send_markdown_reply_to_user_exchange.assert_not_called()
    chat_mock.send_choice_reply_to_user_exchange.assert_not_called()
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_send_reply_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/exchanges/42/send-reply",
        json={
            "type": "markdown",
            "message": "Message!",
            "from_agent_id": 33
        }
    )

    # Assert
    chat_mock.send_markdown_reply_to_user_exchange.assert_not_called()
    chat_mock.send_choice_reply_to_user_exchange.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_send_reply_returns_404_for_nonexistent_exchange(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.send_choice_reply_to_user_exchange.side_effect = NonexistentExchangeError(66)
    chat_mock.send_markdown_reply_to_user_exchange.side_effect = NonexistentExchangeError(55)

    # Act
    res1 = mock_client.post(
        "/api/exchanges/42/send-reply",
        json={
            "type": "markdown",
            "message": "Message!",
            "from_agent_id": 33
        }
    )
    res2 = mock_client.post(
        "/api/exchanges/42/send-reply",
        json={
            "type": "choice",
            "prompt": "Pick a thing",
            "choices": ["choice1", 2],
            "from_agent_id": 33
        }
    )

    # Assert
    chat_mock.send_markdown_reply_to_user_exchange.assert_called_with(
        user_id=1,
        exchange_id=55,
        from_agent_id=33,
        markdown="Message!"
    )
    chat_mock.send_choice_reply_to_user_exchange.assert_called_with(
        user_id=1,
        exchange_id=66,
        from_agent_id=33,
        prompt="Pick a thing",
        choices=["choice1", 2]
    )
    assert res1.status_code == status.HTTP_404_NOT_FOUND
    assert res2.status_code == status.HTTP_404_NOT_FOUND
