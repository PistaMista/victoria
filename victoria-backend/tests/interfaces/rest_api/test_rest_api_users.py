from app.model.user import User, Role
from app.model.action import Action
from app.model.trigger import PollTrigger
from app.services.user import NonexistentUserError, InvalidUserSettingError, UserExistsError, UserDiff
from app.services.auth import NotLoggedInError, AdminRequiredError
from fastapi import status

def test_list_users_returns_200_and_list_of_users_on_valid_request(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.get_all_users.return_value = [
        User(
            id=2,
            username="krystof",
            role=Role.ADMIN
        ),
        User(
            id=3,
            username="john",
            role=Role.USER
        )
    ]

    # Act
    res = mock_client.get("/api/users")

    # Assert
    user_mock.get_all_users.assert_called_with()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 2,
            "username": "krystof",
            "role": "admin"
        },
        {
            "id": 3,
            "username": "john",
            "role": "user"
        }
    ]

def test_list_users_returns_401_when_not_logged_in(mock_client, auth_mock, user_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get("/api/users")

    # Assert
    user_mock.get_all_users.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_users_returns_403_when_not_admin(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get("/api/users")

    # Assert
    user_mock.get_all_users.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_returns_200_and_creates_user_on_valid_request(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.create_user.return_value = 4
    user_mock.get_user_by_id.return_value = User(
        id=4,
        username="mark",
        role=Role.ADMIN,
    )

    # Act
    res = mock_client.post(
        "/api/users",
        json={
            "username": "mark",
            "newPassword": "secret",
            "role": "admin",
            "permittedActions": [2, 3, 4],
            "permittedTriggers": [10, 40]
        }
    )

    # Assert
    user_mock.create_user.assert_called_with(
        username="mark",
        password="secret",
        role=Role.ADMIN,
        permitted_action_ids=[2, 3, 4],
        permitted_trigger_ids=[10, 40]
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 4,
        "username": "mark",
        "role": "admin"
    }

def test_create_user_returns_400_on_username_taken(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.create_user.side_effect = UserExistsError("mark")

    # Act
    res = mock_client.post(
        "/api/users",
        json={
            "username": "mark",
            "newPassword": "secret",
            "role": "admin",
            "permittedActions": [2, 3, 4],
            "permittedTriggers": [10, 40]
        }
    )

    # Assert
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_returns_400_on_specifying_invalid_settings(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.create_user.side_effect = InvalidUserSettingError("")

    # Act
    res = mock_client.post(
        "/api/users",
        json={
            "username": "mark",
            "newPassword": "secret",
            "role": "admin",
            "permittedActions": [2, 3, 4],
            "permittedTriggers": [10, 40]
        }
    )

    # Assert
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_create_user_returns_401_when_not_logged_in(mock_client, auth_mock, user_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/users",
        json={
            "username": "mark",
            "newPassword": "secret",
            "role": "admin",
            "permittedActions": [2, 3, 4],
            "permittedTriggers": [10, 40]
        }
    )

    # Assert
    user_mock.create_user.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_user_returns_403_when_not_admin(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.post(
        "/api/users",
        json={
            "username": "mark",
            "newPassword": "secret",
            "role": "admin",
            "permittedActions": [2, 3, 4],
            "permittedTriggers": [10, 40]
        }
    )

    # Assert
    user_mock.create_user.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_get_user_returns_200_and_user_on_valid_request(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.get_user_by_id.return_value = User(
        id=3,
        username="john",
        password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
        role=Role.ADMIN,
        allowed_actions=[
            Action(
                id=20
            ),
            Action(
                id=40
            )
        ],
        allowed_triggers=[
            PollTrigger(
                id=42
            ),
            PollTrigger(
                id=60
            )
        ]
    )

    # Act
    res = mock_client.get(
        "/api/users/3"
    )

    # Assert
    user_mock.get_user_by_id.assert_called_with(
        id=3
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 3,
        "username": "john",
        "newPassword": "",
        "role": "admin",
        "permittedActions": [20, 40],
        "permittedTriggers": [42, 60]
    }

def test_get_user_returns_401_when_not_logged_in(mock_client, auth_mock, user_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/users/3"
    )

    # Assert
    user_mock.get_user_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_user_returns_403_when_not_admin(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get(
        "/api/users/3"
    )

    # Assert
    user_mock.get_user_by_id.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_update_user_returns_200_and_updates_user_on_valid_request(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.put(
        "/api/users/3",
        json={
            "newPassword": "weee",
            "role": "user",
            "permittedActions": [98, 56, 9]
        }
    )

    # Assert
    user_mock.update_user.assert_called_with(
        id=3,
        changes=UserDiff(
            new_password="weee",
            role=Role.USER,
            permitted_action_ids=[98, 56, 9]
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_update_user_returns_400_on_username_taken(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.update_user.side_effect = UserExistsError("")

    # Act
    res = mock_client.put(
        "/api/users/3",
        json={
            "newPassword": "weee",
            "role": "user",
            "permittedActions": [98, 56, 9]
        }
    )

    # Assert
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_update_user_returns_400_on_specifying_invalid_ids(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.update_user.side_effect = InvalidUserSettingError("")

    # Act
    res = mock_client.put(
        "/api/users/3",
        json={
            "newPassword": "weee",
            "role": "user",
            "permittedActions": [98, 56, 9]
        }
    )

    # Assert
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_update_user_returns_401_when_not_logged_in(mock_client, auth_mock, user_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.put(
        "/api/users/3",
        json={
            "newPassword": "weee",
            "role": "user",
            "permittedActions": [98, 56, 9]
        }
    )

    # Assert
    user_mock.update_user.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_user_returns_403_when_not_admin(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.put(
        "/api/users/3",
        json={
            "newPassword": "weee",
            "role": "user",
            "permittedActions": [98, 56, 9]
        }
    )

    # Assert
    user_mock.update_user.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_update_user_returns_404_for_nonexistent_user(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.update_user.side_effect = NonexistentUserError(20)

    # Act
    res = mock_client.put(
        "/api/users/20",
        json={
            "newPassword": "weee",
            "role": "user",
            "permittedActions": [98, 56, 9]
        }
    )

    # Assert
    user_mock.update_user.assert_called_with(
        id=20,
        changes=UserDiff(
            new_password="weee",
            role=Role.USER,
            permitted_action_ids=[98, 56, 9]
        )
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_returns_200_and_deletes_user_for_valid_request(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.delete("/api/users/42")

    # Assert
    user_mock.delete_user_by_id.assert_called_with(
        id=42
    )
    assert res.status_code == status.HTTP_200_OK

def test_delete_user_returns_401_when_not_logged_in(mock_client, auth_mock, user_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.delete("/api/users/42")

    # Assert
    user_mock.delete_user_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_user_returns_403_when_not_admin(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res= mock_client.delete("/api/users/42")

    # Assert
    user_mock.delete_user_by_id.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_delete_user_returns_404_for_nonexistent_user(mock_client, auth_mock, user_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    user_mock.delete_user_by_id.side_effect = NonexistentUserError(42)

    # Act
    res= mock_client.delete("/api/users/42")

    # Assert
    user_mock.delete_user_by_id.assert_called_with(
        id=42
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
