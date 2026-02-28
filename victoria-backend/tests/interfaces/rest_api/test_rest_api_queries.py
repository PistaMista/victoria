from app.services.auth import NotLoggedInError
from app.services.chat import NonexistentMessageError, QueryAlreadyAnsweredError
from fastapi import status


def test_get_query_answer_returns_200_and_message_answer_on_valid_request(
    mock_client, auth_mock, chat_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_query_answer.return_value = "answeros"

    # Act
    res = mock_client.get("/api/queries/20/answer")

    # Assert
    chat_mock.get_user_query_answer.assert_called_with(user_id=1, message_id=20)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == "answeros"


def test_get_query_answer_returns_401_when_not_logged_in(
    mock_client, auth_mock, chat_mock
):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get("/api/queries/20/answer")

    # Assert
    chat_mock.get_user_query_answer.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_query_answer_returns_404_for_nonexistent_message(
    mock_client, auth_mock, chat_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.get_user_query_answer.side_effect = NonexistentMessageError(20)

    # Act
    res = mock_client.get("/api/queries/20/answer")

    # Assert
    chat_mock.get_user_query_answer.assert_called_with(user_id=1, message_id=20)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_set_query_answer_returns_200_and_sets_message_answer_on_valid_request(
    mock_client, auth_mock, chat_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.post("/api/queries/20/answer", json=300)

    # Assert
    chat_mock.set_user_query_answer.assert_called_with(
        user_id=1, message_id=20, answer=300
    )
    assert res.status_code == status.HTTP_200_OK


def test_set_query_answer_returns_400_for_answered_message(
    mock_client, auth_mock, chat_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.set_user_query_answer.side_effect = QueryAlreadyAnsweredError(20)

    # Act
    res = mock_client.post("/api/queries/20/answer", json=300)

    # Assert
    chat_mock.set_user_query_answer.assert_called_with(
        user_id=1, message_id=20, answer=300
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_set_query_answer_returns_401_when_not_logged_in(
    mock_client, auth_mock, chat_mock
):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post("/api/queries/20/answer", json=300)

    # Assert
    chat_mock.set_user_query_answer.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_set_query_answer_returns_404_for_nonexistent_message(
    mock_client, auth_mock, chat_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    chat_mock.set_user_query_answer.side_effect = NonexistentMessageError(20)

    # Act
    res = mock_client.post("/api/queries/20/answer", json="lol")

    # Assert
    chat_mock.set_user_query_answer.assert_called_with(
        user_id=1, message_id=20, answer="lol"
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
