from fastapi.websockets import WebSocketDisconnect
from app.services.auth import NotLoggedInError, AdminRequiredError
import pytest
from time import sleep


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
        sleep(0.5)


def test_websocket_connect_throws_when_not_logged_in(mock_client, auth_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act / Assert
    with pytest.raises(WebSocketDisconnect):
        with mock_client.websocket_connect("/ws", cookies={"token": "tokenito"}) as _:
            pass

    auth_mock.get_as_non_admin_user.assert_called_once_with("tokenito")


@pytest.mark.timeout(5)
def test_websocket_sends_heartbeat_message_periodically(
    mock_app, mock_client, auth_mock, user
):
    # Arrange
    mock_app.container.config.WS_HEARTBEAT_INTERVAL.override(0.1)
    mock_app.container.config.WS_HEARTBEAT_TIMEOUT.override(99999.0)
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act / Assert
    with mock_client.websocket_connect("/ws", cookies={"token": "tokenito"}) as ws:
        for _ in range(3):
            ping = ws.receive_json()
            assert ping == {"type": "ping"}


@pytest.mark.timeout(5)
def test_websocket_stays_open_if_client_replies_to_heartbeat(
    mock_app, mock_client, auth_mock, user
):
    # Arrange
    mock_app.container.config.WS_HEARTBEAT_INTERVAL.override(0.2)
    mock_app.container.config.WS_HEARTBEAT_TIMEOUT.override(0.7)
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act / Assert
    with mock_client.websocket_connect("/ws", cookies={"token": "tokenito"}) as ws:
        for i in range(5):
            sleep(0.2)
            obj = ws.receive_json()

            if obj == {"type": "ping"}:
                ws.send_json({"type": "pong"})
            else:
                i -= 1


@pytest.mark.timeout(5)
def test_websocket_closes_if_client_not_replies_to_heartbeat(
    mock_app, mock_client, auth_mock, user
):
    # Arrange
    mock_app.container.config.WS_HEARTBEAT_INTERVAL.override(0.3)
    mock_app.container.config.WS_HEARTBEAT_TIMEOUT.override(0.5)
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act / Assert
    with pytest.raises(WebSocketDisconnect):
        with mock_client.websocket_connect("/ws", cookies={"token": "tokenito"}) as ws:
            for _ in range(3):
                ws.receive_json()
                sleep(0.7)
                ws.send_json({"type": "ping"})
