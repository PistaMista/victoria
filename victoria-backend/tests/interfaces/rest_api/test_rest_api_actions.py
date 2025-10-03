from app.model.action import Action
from app.services.auth import NotLoggedInError, AdminRequiredError
from fastapi import status

def test_list_actions_for_user_returns_200_and_list_of_user_allowed_actions_on_valid_request(mock_client, auth_mock, action_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    action_mock.get_user_permitted_actions.return_value = [
        Action(
            id=1,
            function_name="add_to_calendar",
            function_param_schema={},
            function_source_code="",
            function_docstring="",
            repository_id=3
        ),
        Action(
            id=2,
            function_name="search_web",
            function_param_schema={},
            function_source_code="",
            function_docstring="",
            repository_id=4
        )
    ]

    # Act
    res = mock_client.get(
            '/api/actions',
            cookies={ "token": "tok" }
    )

    # Assert
    action_mock.get_user_permitted_actions.assert_called_with(1)
    action_mock.get_all_actions.assert_not_called()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "repoId": 3,
            "name": "add_to_calendar",
            "displayName": "Add to calendar"
        },
        {
            "id": 2,
            "repoId": 4,
            "name": "search_web",
            "displayName": "Search web"
        }
    ]


def test_list_actions_for_user_returns_401_when_not_signed_in(mock_client, auth_mock, action_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/actions',
        cookies={ "token": "tok" }
    )

    # Assert
    action_mock.get_user_permitted_actions.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_all_actions_returns_200_and_list_of_all_actions_on_valid_request(mock_client, auth_mock, action_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    action_mock.get_all_actions.return_value = [
        Action(
            id=1,
            function_name="add_to_calendar",
            function_param_schema={},
            function_source_code="",
            function_docstring="",
            repository_id=3
        ),
        Action(
            id=2,
            function_name="search_web",
            function_param_schema={},
            function_source_code="",
            function_docstring="",
            repository_id=4
        )
    ]

    # Act
    res = mock_client.get(
        '/api/actions/all',
        cookies={ "token": "tok" }
    )

    # Assert
    action_mock.get_all_actions.assert_called_with()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "repoId": 3,
            "name": "add_to_calendar",
            "displayName": "Add to calendar"
        },
        {
            "id": 2,
            "repoId": 4,
            "name": "search_web",
            "displayName": "Search web"
        }
    ]

def test_list_all_actions_returns_401_when_not_signed_in(mock_client, auth_mock, action_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/actions/all',
        cookies={ "token": "tok" }
    )

    # Assert
    action_mock.get_all_actions.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_all_actions_returns_403_when_not_admin(mock_client, auth_mock, action_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get(
        '/api/actions/all',
        cookies={ "token": "tok" }
    )

    # Assert
    action_mock.get_all_actions.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

