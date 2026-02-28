import pytest
from fastapi import status
from app.model.user import User, Role
from app.model.action_repository import ActionRepository
from app.services.action import NonexistentActionRepositoryError, ActionRepositoryDiff
from app.services.auth import AdminRequiredError, NotLoggedInError


def test_list_repos_returns_200_with_repo_list_for_valid_request(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    action_mock.get_all_action_repositories.return_value = [
        ActionRepository(id=1, name="Basic", url="seznam.cz", actions=[]),
        ActionRepository(id=2, name="Homelab Admin", url="lol.cz", actions=[]),
    ]

    # Act
    res = mock_client.get("/api/action-repos", cookies={"token": "tokenito"})

    # Assert
    action_mock.get_all_action_repositories.assert_called_with()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {"id": 1, "name": "Basic", "url": "seznam.cz"},
        {"id": 2, "name": "Homelab Admin", "url": "lol.cz"},
    ]


def test_list_repos_returns_401_when_not_logged_in(mock_client, auth_mock, action_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get("/api/action-repos", cookies={"token": "tokenito"})

    # Assert
    action_mock.get_all_action_repositories.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_repos_returns_403_when_not_admin(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get("/api/action-repos", cookies={"token": "tokenito"})

    # Assert
    action_mock.get_all_action_repositories.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_get_repo_returns_200_with_repo_for_valid_request(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    action_mock.get_action_repository_by_id.return_value = ActionRepository(
        id=3, name="Basic", url="MYURL"
    )

    # Act
    res = mock_client.get("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.get_action_repository_by_id.assert_called_with(3)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"id": 3, "name": "Basic", "url": "MYURL"}


def test_get_repo_returns_401_when_not_logged_in(mock_client, auth_mock, action_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.get_action_repository_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_repo_returns_403_when_not_admin(mock_client, auth_mock, action_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.get_action_repository_by_id.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_get_repo_returns_404_on_nonexistent_repo(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    action_mock.get_action_repository_by_id.side_effect = (
        NonexistentActionRepositoryError(3)
    )

    # Act
    res = mock_client.get("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.get_action_repository_by_id.assert_called_with(3)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_repo_returns_200_and_creates_repo_for_valid_request(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.post(
        "/api/action-repos",
        json={"id": 0, "name": "Wooo", "url": "Weee"},
        cookies={"token": "tokenito"},
    )

    # Assert
    action_mock.add_action_repository.assert_called_with(name="Wooo", url="Weee")
    assert res.status_code == status.HTTP_200_OK


def test_create_repo_returns_401_when_not_logged_in(
    mock_client, auth_mock, action_mock
):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/action-repos",
        json={"id": 0, "name": "Wooo", "url": "Weee"},
        cookies={"token": "tokenito"},
    )

    # Assert
    action_mock.add_action_repository.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_repo_returns_403_when_not_admin(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.post(
        "/api/action-repos",
        json={"id": 0, "name": "Wooo", "url": "Weee"},
        cookies={"token": "tokenito"},
    )

    # Assert
    action_mock.add_action_repository.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_repo_returns_200_and_updates_repo_for_simple_request(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.put(
        "/api/action-repos/3", json={"name": "Lab"}, cookies={"token": "tokenito"}
    )

    # Assert
    action_mock.update_action_repository.assert_called_with(
        3, ActionRepositoryDiff(name="Lab")
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == True


def test_update_repo_returns_200_and_updates_repo_proper_setters_for_complex_request(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.put(
        "/api/action-repos/3",
        json={"name": "Lab", "url": "new"},
        cookies={"token": "tokenito"},
    )

    # Assert
    action_mock.update_action_repository.assert_called_with(
        3, ActionRepositoryDiff(name="Lab", url="new")
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == True


def test_update_repo_returns_401_when_not_logged_in(
    mock_client, auth_mock, action_mock
):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.put(
        "/api/action-repos/3",
        json={"name": "Lab", "url": "new"},
        cookies={"token": "tokenito"},
    )

    # Assert
    action_mock.update_action_repository.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_repo_returns_403_when_not_admin(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.put(
        "/api/action-repos/3",
        json={"name": "Lab", "url": "new"},
        cookies={"token": "tokenito"},
    )

    # Assert
    action_mock.update_action_repository.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_repo_returns_404_on_nonexistent_repo(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    action_mock.update_action_repository.side_effect = NonexistentActionRepositoryError(
        3
    )

    # Act
    res = mock_client.put(
        "/api/action-repos/3",
        json={"name": "Lab", "url": "new"},
        cookies={"token": "tokenito"},
    )

    # Assert
    action_mock.update_action_repository.assert_called_with(
        3, ActionRepositoryDiff(name="Lab", url="new")
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_repo_returns_200_and_deletes_repo_for_valid_request(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.delete("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.remove_action_repository.assert_called_with(3)
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == True


def test_delete_repo_returns_401_when_not_logged_in(
    mock_client, auth_mock, action_mock
):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.delete("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.remove_action_repository.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_repo_returns_403_when_not_admin(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.delete("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.remove_action_repository.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_delete_repo_returns_404_for_nonexistent_repo(
    mock_client, auth_mock, action_mock, user
):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    action_mock.remove_action_repository.side_effect = NonexistentActionRepositoryError(
        3
    )

    # Act
    res = mock_client.delete("/api/action-repos/3", cookies={"token": "tokenito"})

    # Assert
    action_mock.remove_action_repository.assert_called_with(3)
    assert res.status_code == status.HTTP_404_NOT_FOUND
