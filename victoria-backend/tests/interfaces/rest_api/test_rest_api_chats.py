from app.services.auth import NotLoggedInError
from app.services.chat import NonexistentChatError, ChatOptionsDiff
from app.model.user import User
from app.model.agent import Agent
from app.model.monologue import Monologue
from app.model.action import Action
from fastapi import status
import threading
import time
from datetime import datetime

def test_list_chats_returns_200_and_list_of_chats_for_current_user_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chats.return_value = [
        Chat(
            id=1,
            title="System admin",
            summary="Chat about system administration."
        ),
        Chat(
            id=2,
            title="Language learning",
            summary="Discussing ways to learn languages effectively."
        )
    ]

    # Act
    res = mock_client.get(
        '/api/chats',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.get_user_chats.assert_called_with(
        user_id=1
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "title": "System admin",
            "summary": "Chat about system administration."
        },
        {
            "id": 2,
            "title": "Language learning",
            "summary": "Discussing ways to learn languages effectively."
        }
    ]

def test_list_chats_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/chats',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.get_user_chats.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_chat_returns_200_and_creates_chat_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.create_user_chat.return_value = 3
    chat_mock.get_user_chat.return_value = Chat(
        id=3,
        title="New chat",
        summary="No summary"
    )

    # Act
    res = mock_client.post(
        '/api/chats',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.create_user_chat.assert_called_with(
        user_id=1
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 3,
        "title": "New chat",
        "summary": "No summary"
    }

def test_create_chat_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        '/api/chats',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.create_user_chat.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_chat_returns_200_and_deletes_chat_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.delete(
        '/api/chats/57',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.remove_user_chat.assert_called_with(
        user_id=1,
        chat_id=57
    )
    assert res.status_code == status.HTTP_200_OK


def test_delete_chat_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.delete(
        '/api/chats/57',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.remove_user_chat.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_chat_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.remove_user_chat.side_effect = NonexistentChatError(57)

    # Act
    res = mock_client.delete(
        '/api/chats/57',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.remove_user_chat.assert_called_with(
        user_id=1,
        chat_id=57
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_list_receivers_returns_200_and_list_of_receivers_for_current_user_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat_receivers.return_value = ['general', 'technical']

    # Act
    res = mock_client.get(
        '/api/chats/receivers',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.get_user_chat_receivers.assert_called_with(user_id=1)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == ['general', 'technical']

def test_list_receivers_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/chats/receivers',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.get_user_chat_receivers.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_duplicate_chat_returns_200_and_duplicates_chat_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.duplicate_user_chat.return_value = 75

    # Act
    res = mock_client.post(
        '/api/chats/42/duplicate',
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.duplicate_user_chat.assert_called_with(
        user_id=1,
        chat_id=42
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == 75

def test_duplicate_chat_returns_200_and_duplicates_chat_up_to_exchange_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.duplicate_user_chat.return_value = 75

    # Act
    res = mock_client.post(
        '/api/chats/42/duplicate',
        json={
            "toExchange": 101
        },
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.duplicate_user_chat.assert_called_with(
        user_id=1,
        chat_id=42,
        last_exchange_id=101
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == 75

def test_duplicate_chat_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        '/api/chats/42/duplicate',
        json={
            "toExchange": 101
        },
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.duplicate_user_chat.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_duplicate_chat_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.duplicate_user_chat.side_effect = NonexistentChatError(42)

    # Act
    res = mock_client.post(
        '/api/chats/42/duplicate',
        json={
            "toExchange": 101
        },
        cookies={"token": "tok"}
    )

    # Assert
    chat_mock.duplicate_user_chat.assert_called_with(
        user_id=1,
        chat_id=42,
        last_exchange_id=101
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_send_message_to_chat_returns_200_and_creates_exchange_with_markdown_message_on_user_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.send_markdown_message_to_user_chat.return_value = 10

    # Act
    res = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "type": "markdown",
            "message": "Message!"
        }
    )

    # Assert
    chat_mock.send_markdown_message_to_user_chat.assert_called_with(
        user_id=1,
        chat_id=4,
        from_agent_id=None,
        markdown="Message!"
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "exchangeId": 10
    }

def test_send_message_to_chat_returns_200_and_creates_exchange_with_markdown_message_on_agent_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.send_markdown_message_to_user_chat.return_value = 10

    # Act
    res = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "type": "markdown",
            "message": "Message!",
            "from_agent_id": 33
        }
    )

    # Assert
    chat_mock.send_markdown_message_to_user_chat.assert_called_with(
        user_id=1,
        chat_id=4,
        from_agent_id=33,
        markdown="Message!"
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "exchangeId": 10
    }

def test_send_message_to_chat_returns_200_creates_exchange_with_choice_prompt_and_returns_query_id_on_user_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.send_choice_message_to_user_chat.return_value = (42, 120)

    # Act
    res = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "type": "choice_prompt",
            "choices": ['lol', 'weee']
        }
    )

    # Assert
    chat_mock.send_choice_message_to_user_chat.assert_called_with(
        user_id=1,
        chat_id=4,
        from_agent_id=None,
        choices=['lol', 'weee']
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "exchangeId": 42,
        "queryId": 120
    }

def test_send_message_to_chat_returns_200_creates_exchange_with_choice_prompt_and_returns_query_id_on_agent_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.send_choice_message_to_user_chat.return_value = (42, 120)

    # Act
    res = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "type": "choice_prompt",
            "choices": ['lol', 'weee'],
            "from_agent_id": 88
        }
    )

    # Assert
    chat_mock.send_choice_message_to_user_chat.assert_called_with(
        user_id=1,
        chat_id=4,
        from_agent_id=88,
        choices=['lol', 'weee']
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "exchangeId": 42,
        "queryId": 120
    }

def test_send_message_to_chat_returns_200_and_assumes_markdown_message_when_type_unspecified_on_user_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user = user
    chat_mock.send_markdown_message_to_user_chat.return_value = 99

    # Act
    res = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "message": "Weee"
        }
    )

    # Assert
    chat_mock.send_markdown_message_to_user_chat.assert_called_with(
        user_id=1,
        chat_id=4,
        from_agent_id=None,
        markdown="Weee",
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "exchangeId": 99
    }

def test_send_message_to_chat_returns_400_when_unknown_message_type_specified(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "type": "something",
            "message": "Weee"
        }
    )

    # Assert
    chat_mock.send_markdown_message_to_user_chat.assert_not_called()
    chat_mock.send_choice_message_to_user_chat.assert_not_called()
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_send_message_to_chat_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "message": "Weee"
        }
    )

    # Assert
    chat_mock.send_markdown_message_to_user_chat.assert_not_called()
    chat_mock.send_choice_message_to_user_chat.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_send_message_to_chat_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.send_markdown_message_to_user_chat.side_effect = NonexistentChatError(4)
    chat_mock.send_choice_message_to_user_chat.side_effect = NonexistentChatError(4)

    # Act
    res1 = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "type": "markdown",
            "message": "Weee"
        }
    )
    res2 = mock_client.post(
        '/api/chats/4/send-message',
        json={
            "type": "choice_prompt",
            "choices": [10, 20]
        }
    )

    # Assert
    chat_mock.send_markdown_message_to_user_chat.assert_called_with(
        user_id=1,
        chat_id=4,
        from_agent_id=None,
        markdown="Weee"
    )
    chat_mock.send_choice_message_to_user_chat.assert_called_with(
        user_id=1,
        chat_id=4,
        from_agent_id=None,
        choices=[10, 20]
    )
    assert res1.status_code == status.HTTP_404_NOT_FOUND
    assert res2.status_code == status.HTTP_404_NOT_FOUND

def test_list_exchanges_returns_200_and_list_of_exchanges_when_new_exchanges_available(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat_exchanges_after.return_value = [
        Exchange(
            id=2,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1000),
            user_message=MarkdownMessage(
                id=1,
                timestamp=datetime.fromtimestamp(1000),
                exchange_id=2,
                sending_user=User(
                    username="John"
                ),
                sending_agent=None,
                markdown="Hello?"
            ),
            monologues=[
                Monologue(
                    id=1
                ),
                Monologue(
                    id=2
                )
            ]
        ),
        Exchange(
            id=3,
            chat_id=4,
            timestamp=datetime.fromtimestamp(1200),
            user_message=None,
            monologues=[
                Monologue(
                    id=3
                )
            ]
        )
    ]

    # Act
    res = mock_client.get(
        '/api/chats/4/exchanges',
        params={
            "after": 1000
        }
    )

    # Assert
    chat_mock.get_user_chat_exchanges_after.assert_called_with(
        user_id=1,
        chat_id=4,
        after=1000
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 2,
            "chatId": 4,
            "timestamp": 1000,
            "userMessage": {
                "id": 1,
                "senderName": "John",
                "timestamp": 1000,
                "content": {
                    "type": "markdown",
                    "markdownText": "Hello?"
                }
            },
            "monologueIds": [1, 2]
        },
        {
            "id": 3,
            "chatId": 4,
            "timestamp": 1200,
            "userMessage": None,
            "monologueIds": [3]
        }
    ]

def test_list_exchanges_waits_until_new_exchanges_are_available_before_returning_200_and_data(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat_exchanges_after.return_value = []
    def data_source():
        time.sleep(2)
        chat_mock.get_user_chat_exchanges_after.return_value = [
            Exchange(
                id=3,
                chat_id=4,
                timestamp=datetime.fromtimestamp(1700),
                user_message=None,
                monologues=[
                    Monologue(
                        id=320
                    )
                ]
            )
        ]

    source_thread = threading.Thread(target=data_source)
    source_thread.start()


    # Act
    res = mock_client.get(
        '/api/chats/4/exchanges',
        params={
            "after": 1000
        }
    )
    source_thread.join()

    # Assert
    chat_mock.get_user_chat_exchanges_after.assert_called_with(
        user_id=1,
        chat_id=4,
        after=1000
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 3,
            "chatId": 4,
            "timestamp": 1700,
            "userMessage": None,
            "monologueIds": [320]
        }
    ]

def test_list_exchanges_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/chats/4/exchanges',
        params={
            "after": 1000
        }
    )

    # Assert
    chat_mock.get_user_chat_exchanges_after.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_exchanges_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat_exchanges_after.side_effect = NonexistentChatError(3)

    # Act
    res = mock_client.get(
        '/api/chats/4/exchanges',
        params={
            "after": 1000
        }
    )

    # Assert
    chat_mock.get_user_chat_exchanges_after.assert_called_with(
        user_id=1,
        chat_id=4,
        after=1000
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_get_chat_options_returns_200_and_chat_options_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat.return_value = Chat(
        id=3,
        title="Chat",
        summary="Summary",
        receiver="general",
        allowed_actions=[
            Action(id=15),
            Action(id=90)
        ]
    )

    # Act
    res = mock_client.get(
        '/api/chats/4/options'
    )

    # Assert
    chat_mock.get_user_chat.assert_called_with(
        user_id=1,
        chat_id=4
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "receiver": "general",
        "enabledActionIds": [15, 90]
    }

def test_get_chat_options_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/chats/4/options'
    )

    # Assert
    chat_mock.get_user_chat.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_chat_options_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat.side_effect = NonexistentChatError(4)

    # Act
    res = mock_client.get(
        '/api/chats/4/options'
    )

    # Assert
    chat_mock.get_user_chat.assert_called_with(
        user_id=1,
        chat_id=4
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_set_chat_options_returns_200_and_updates_chat_options_on_simple_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.put(
        '/api/chats/4/options',
        json={
            "receiver": "new"
        }
    )

    # Assert
    chat_mock.update_user_chat_options.assert_called_with(
        user_id=1,
        chat_id=4,
        options=ChatOptionsDiff(
            receiver="New"
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_set_chat_options_returns_200_and_updates_chat_options_on_complex_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.put(
        '/api/chats/4/options',
        json={
            "receiver": "new",
            "enabledActionIds": [84, 24]
        }
    )

    # Assert
    chat_mock.update_user_chat_options.assert_called_with(
        user_id=1,
        chat_id=4,
        options=ChatOptionsDiff(
            receiver="New",
            enabled_action_ids=[84, 24]
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_set_chat_options_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.put(
        '/api/chats/4/options',
        json={
            "receiver": "new",
            "enabledActionIds": [84, 24]
        }
    )

    # Assert
    chat_mock.update_user_chat_options.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_set_chat_options_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.update_user_chat_options.side_effect = NonexistentChatError(4)

    # Act
    res = mock_client.put(
        '/api/chats/4/options',
        json={
            "receiver": "blabla"
        }
    )

    # Assert
    chat_mock.update_user_chat_options.assert_called_with(
        user_id=1,
        chat_id=4,
        options=ChatOptionsDiff(
            receiver="blabla"
        )
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_set_chat_summary_returns_200_and_set_chat_summary_for_valid_requests(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.post(
        '/api/chats/50/summary',
        json="My new summary!"
    )

    # Assert
    chat_mock.set_user_chat_summary.assert_called_with(
        user_id=1,
        chat_id=50,
        summary="My new summary!"
    )
    assert res.status_code == status.HTTP_200_OK

def test_set_chat_summary_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        '/api/chats/50/summary',
        json="Lol"
    )

    # Assert
    chat_mock.set_user_chat_summary.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_set_chat_summary_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.set_user_chat_summary.side_effect = NonexistentChatError(50)

    # Act
    res = mock_client.post(
        '/api/chats/50/summary',
        json="Lol"
    )

    # Assert
    chat_mock.set_user_chat_summary.assert_called_with(
        user_id=1,
        chat_id=50,
        summary="My new summary!"
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND



def test_get_chat_history_returns_200_and_all_chat_messages_for_valid_requests(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat_messages.return_value = [
        MarkdownMessage(
            id=1,
            sending_user=User(
                username="John"
            ),
            sending_agent=None,
            markdown="Hello!"
        ),
        MarkdownMessage(
            id=2,
            sending_user=None,
            sending_agent=Agent(
                name="Cook"
            ),
            markdown="What can I help you with?"
        ),
        MarkdownMessage(
            id=3,
            sending_user=User(
                username="John"
            ),
            sending_agent=None,
            markdown="Give me a recipe for pretzels"
        ),
        MarkdownMessage(
            id=4,
            sending_user=None,
            sending_agent=Agent(
                name="Cook"
            ),
            markdown="Here it is"
        )
    ]

    # Act
    res = mock_client.get(
        '/api/chats/42/history'
    )

    # Assert
    chat_mock.get_user_chat_messages.assert_called_with(
        user_id=1,
        chat_id=42
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json == [
        {
            "role": "user",
            "message": "Hello!"
        },
        {
            "role": "assistant",
            "agentName": "Cook",
            "message": "What can I help you with?"
        },
        {
            "role": "user",
            "message": "Give me a recipe for pretzels"
        },
        {
            "role": "assistant",
            "agentName": "Cook",
            "message": "Here it is"
        }
    ]

def test_get_chat_history_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/chats/42/history'
    )

    # Assert
    chat_mock.get_user_chat_messages.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_chat_history_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat_messages.side_effect = NonexistentChatError(42)

    # Act
    res = mock_client.get(
        '/api/chats/42/history'
    )

    # Assert
    chat_mock.get_user_chat_messages.assert_called_with(
        user_id=1,
        chat_id=42
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_get_chat_returns_200_and_basic_chat_info_on_valid_request(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat.return_value = Chat(
        id=3,
        title="Dogs",
        summary="Chat about dogs",
        receiver="general",
        allowed_actions=[
            Action(id=15),
            Action(id=90)
        ]
    )

    # Act
    res = mock_client.get(
        '/api/chats/42'
    )

    # Assert
    chat_mock.get_user_chat.assert_called_with(
        user_id=1,
        chat_id=42
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 42,
        "title": "Dogs",
        "summary": "Chat about dogs"
    }

def test_get_chat_returns_401_when_not_logged_in(mock_client, auth_mock, chat_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/chats/42'
    )

    # Assert
    chat_mock.get_user_chat.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_chat_returns_404_for_nonexistent_chat(mock_client, auth_mock, chat_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_chat.side_effect = NonexistentChatError(42)

    # Act
    res = mock_client.get(
        '/api/chats/42'
    )

    # Assert
    chat_mock.get_user_chat.assert_called_with(
        user_id=1,
        chat_id=42
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
