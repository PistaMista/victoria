from app.services.auth import NotLoggedInError, AdminRequiredError
from app.services.llm import NonexistentModelError
from app.model.language_model import LanguageModel
from app.model.llm_connection import OllamaConnection
from fastapi import status

def test_list_enabled_models_returns_200_and_lists_enabled_models_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    llm_mock.get_enabled_models.return_value = [
        LanguageModel(
            id=1,
            name="gemma3:12b",
            enabled=True,
            connection=OllamaConnection(
                id=33,
                name="Homelab",
                url="seznam.cz"
            )
        ),
        LanguageModel(
            id=20,
            name="llama3.1:8b",
            enabled=True,
            connection=OllamaConnection(
                id=20,
                name="Commercial",
                url="lol.com"
            )
        )
    ]

    # Act
    res = mock_client.get(
        "/api/models/enabled"
    )

    # Assert
    llm_mock.get_enabled_models.assert_called_with()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "connectionId": 33,
            "name": "gemma3:12b",
            "enabled": True
        },
        {
            "id": 20,
            "connectionId": 20,
            "name": "llama3.1:8b",
            "enabled": True
        }
    ]

def test_list_enabled_models_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/models/enabled"
    )

    # Assert
    llm_mock.get_enabled_user_models.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_all_models_returns_200_and_lists_all_models_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    llm_mock.get_all_models.return_value = [
        LanguageModel(
            id=1,
            name="gemma3:12b",
            enabled=False,
            connection=OllamaConnection(
                id=33,
                name="Homelab",
                url="seznam.cz"
            )
        )
    ]

    # Act
    res = mock_client.get(
        "/api/models/all"
    )

    # Assert
    llm_mock.get_all_models.assert_called_with()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "connectionId": 33,
            "name": "gemma3:12b",
            "enabled": False
        }
    ]

def test_list_all_models_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/models/all"
    )

    # Assert
    llm_mock.get_all_models.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_enable_model_returns_200_and_enables_model_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.post(
        "/api/models/3/enable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_called_with(
        model_id=3,
        enabled=True
    )
    assert res.status_code == status.HTTP_200_OK

def test_enable_model_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/models/3/enable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_enable_model_returns_403_when_not_admin(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.post(
        "/api/models/3/enable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_enable_model_returns_404_for_nonexistent_model(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.set_model_enabled_by_id.side_effect = NonexistentModelError(3)

    # Act
    res = mock_client.post(
        "/api/models/3/enable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_called_with(
        model_id=3,
        enabled=True
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_disable_model_returns_200_and_disables_model_on_valid_request(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.post(
        "/api/models/3/disable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_called_with(
        model_id=3,
        enabled=False
    )
    assert res.status_code == status.HTTP_200_OK

def test_disable_model_returns_401_when_not_logged_in(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/models/3/disable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_disable_model_returns_403_when_not_admin(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.post(
        "/api/models/3/disable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_disable_model_returns_404_for_nonexistent_model(mock_client, auth_mock, llm_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    llm_mock.set_model_enabled_by_id.side_effect = NonexistentModelError(3)

    # Act
    res = mock_client.post(
        "/api/models/3/disable"
    )

    # Assert
    llm_mock.set_model_enabled_by_id.assert_called_with(
        model_id=3,
        enabled=False
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
