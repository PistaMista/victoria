from fastapi.websockets import WebSocketDisconnect
from app.services.auth import NotLoggedInError, AdminRequiredError
import pytest


def test_websocket_connect_succeeds_for_valid_connection_request(
    mock_client, auth_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    with mock_client.websocket_connect("/ws", cookies={"token": "tokenito"}) as ws:
        # Assert
        assert ws is not None
        auth_mock.get_as_non_admin_user.assert_called_once_with("tokenito")


def test_websocket_connect_throws_when_not_logged_in(mock_client, auth_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act / Assert
    with pytest.raises(WebSocketDisconnect):
        with mock_client.websocket_connect("/ws", cookies={"token": "tokenito"}) as _:
            pass

    auth_mock.get_as_non_admin_user.assert_called_once_with("tokenito")
