from app.services.llm import NonexistentConnectionError, OllamaConnectionDiff, OllamaCommunicationError
from app.services.auth import NotLoggedInError, AdminRequiredError
from app.model.llm_connection import OllamaConnection
from fastapi import status

def test_list_connections_returns_200_and_list_of_connections_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.get_all_connections.return_value = [
            OllamaConnection(
                id=1,
                name="Homelab",
                url="seznam.cz"
            ),
            OllamaConnection(
                id=2,
                name="Basics",
                url="lol.cz"
            )
    ]

    # Act
    res = mock_client.get("/api/connections")

    # Assert
    llm_mock.get_all_connections.assert_called_with()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "name": "Homelab"
        },
        {
            "id": 2,
            "name": "Basics"
        }
    ]


def test_list_connections_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get("/api/connections")

    # Assert
    llm_mock.get_all_connections.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_connections_returns_403_when_not_admin(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get("/api/connections")

    # Assert
    llm_mock.get_all_connections.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_create_connection_returns_200_and_creates_connection_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.add_ollama_connection.return_value = 1
    llm_mock.get_connection_by_id.return_value = OllamaConnection(
        id=1,
        name="New",
        url="woo"
    )

    # Act
    res = mock_client.post(
            "/api/connections",
            json={
                "id": 0,
                "name": "New",
                "url": "woo"
            }
    )

    # Assert
    llm_mock.add_ollama_connection.assert_called_with(
        name="New",
        url="woo"
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 1,
        "name": "New"
    }

def test_create_connection_returns_400_on_ollama_communication_failure(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.add_ollama_connection.side_effect = OllamaCommunicationError()

    # Act
    res = mock_client.post(
            "/api/connections",
            json={
                "id": 0,
                "name": "New",
                "url": "woo"
            }
    )

    # Assert
    llm_mock.add_ollama_connection.assert_called_with(
        name="New",
        url="woo"
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_create_connection_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/connections",
        json={
            "id": 0,
            "name": "Site",
            "url": "site"
        }
    )

    # Assert
    llm_mock.add_ollama_connection.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_connection_returns_403_when_not_admin(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.post(
        "/api/connections",
        json={
            "id": 0,
            "name": "Site",
            "url": "site"
        }
    )

    # Assert
    llm_mock.add_ollama_connection.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_get_connection_returns_200_and_connection_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.get_connection_by_id.return_value = OllamaConnection(
        id=1,
        name="Conn",
        url="conn.com"
    )

    # Act
    res = mock_client.get("/api/connections/1")

    # Assert
    llm_mock.get_connection_by_id.assert_called_with(1)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 1,
        "name": "Conn",
        "url": "conn.com"
    }

def test_get_connection_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get("/api/connections/42")

    # Assert
    llm_mock.get_connection_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_connection_returns_403_when_not_admin(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get("/api/connections/42")

    # Assert
    llm_mock.get_connection_by_id.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_get_connection_returns_404_for_nonexistent_connection(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.get_connection_by_id.side_effect = NonexistentConnectionError(1)

    # Act
    res = mock_client.get("/api/connections/1")

    # Assert
    llm_mock.get_connection_by_id.assert_called_with(1)
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_update_connection_returns_200_and_updates_connection_on_simple_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.put(
        "/api/connections/50",
        json={
            "name": "New"
        }
    )

    # Assert
    llm_mock.update_ollama_connection.assert_called_with(
        id=50,
        changes=OllamaConnectionDiff(
            name="New"
        )
    )
    assert res.status_code == status.HTTP_200_OK



def test_update_connection_returns_200_and_updates_connection_on_complex_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.put(
        "/api/connections/50",
        json={
            "name": "NEW",
            "url": "localhost:2999"
        }
    )

    # Assert
    llm_mock.update_ollama_connection.assert_called_with(
        id=50,
        changes=OllamaConnectionDiff(
            name="NEW",
            url="localhost:2999"
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_update_connection_returns_400_on_ollama_communication_failure(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.update_ollama_connection.side_effect = OllamaCommunicationError()

    # Act
    res = mock_client.put(
        "/api/connections/50",
        json={
            "name": "NEW",
            "url": "localhost:2999"
        }
    )

    # Assert
    llm_mock.update_ollama_connection.assert_called_with(
        id=50,
        changes=OllamaConnectionDiff(
            name="NEW",
            url="localhost:2999"
        )
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_update_connection_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.put(
        "/api/connections/50",
        json={
            "name": "NEW",
            "url": "localhost:2999"
        }
    )

    # Assert
    llm_mock.update_ollama_connection.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    

def test_update_connection_returns_403_when_not_admin(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.put(
        "/api/connections/50",
        json={
            "name": "NEW",
            "url": "localhost:2999"
        }
    )

    # Assert
    llm_mock.update_ollama_connection.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_update_connection_returns_404_for_nonexistent_connection(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.update_ollama_connection.side_effect = NonexistentConnectionError(50)

    # Act
    res = mock_client.put(
        "/api/connections/50",
        json={
            "name": "NEW",
            "url": "localhost:2999"
        }
    )

    # Assert
    llm_mock.update_ollama_connection.assert_called_with(
        id=50,
        changes=OllamaConnectionDiff(
            name="NEW",
            url="localhost:2999"
        )
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_connection_returns_200_and_deletes_connection_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.delete("/api/connections/50")

    # Assert
    llm_mock.remove_connection.assert_called_with(id=50)
    assert res.status_code == status.HTTP_200_OK

def test_delete_connection_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.delete("/api/connections/50")

    # Assert
    llm_mock.remove_connection.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_connection_returns_403_when_not_admin(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.delete("/api/connections/50")

    # Assert
    llm_mock.remove_connection.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_delete_connection_returns_404_for_nonexistent_connection(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.remove_connection.side_effect = NonexistentConnectionError(50)

    # Act
    res = mock_client.delete("/api/connections/50")

    # Assert
    llm_mock.remove_connection.assert_called_with(id=50)
    assert res.status_code == status.HTTP_404_NOT_FOUND
