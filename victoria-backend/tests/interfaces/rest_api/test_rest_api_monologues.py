from app.services.auth import NotLoggedInError
from app.services.monologues import NonexistentMonologueError
from app.model.event import Event
from app.model.monologue import Monologue, MonologueStatus
from app.model.agent import Agent
from app.model.thought import Thought
from app.model.invocation import Invocation
from datetime import datetime
from fastapi import status

def test_list_monologues_returns_200_and_lists_monologues_on_valid_request(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    monologue_mock.get_user_monologues.return_value = [
        Monologue(
            id=1,
            title="Research thesis ideas",
            summary="Searching the web for sources",
            status=MonologueStatus.RUNNING,
            agent_id=20,
            agent=Agent(
                id=20
            )
        ),
        Monologue(
            id=172,
            title="Generate recipes for the week",
            summary="Checking available ingredients",
            status=MonologueStatus.PENDING,
            agent_id=8,
            agent=Agent(
                id=8
            )
        )
    ]

    # Act
    res = mock_client.get(
        "/api/monologues"
    )

    # Assert
    monologue_mock.get_user_monologues.assert_called_with(
        user_id=1
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "agentId": 20,
            "status": "RUNNING",
            # TODO: Implement start timestamps for Monologues
            "startTimestamp": 0,
            "title": "Research thesis ideas",
            "summary": "Searching the web for sources"
        },
        {
            "id": 172,
            "agentId": 8,
            "status": "PENDING",
            "startTimestamp": 0,
            "title": "Generate recipes for the week",
            "summary": "Checking available ingredients"
        }
    ]

def test_list_monologues_returns_401_when_not_signed_in(mock_client, auth_mock, monologue_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/monologues"
    )

    # Assert
    monologue_mock.get_user_monologues.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_monologue_returns_200_and_monologue_on_valid_request(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    monologue_mock.get_user_monologue.return_value = Monologue(
        id=1337,
        title="Yo dawg",
        summary="Summery",
        status=MonologueStatus.FAILURE,
        agent_id=600,
        agent=Agent(
            id=600
        )
    )

    # Act
    res = mock_client.get(
        "/api/monologues/1337"
    )

    # Assert
    monologue_mock.get_user_monologue.assert_called_with(
        user_id=1,
        monologue_id=1337
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 1337,
        "agentId": 600,
        # TODO: Implement timestamps for Monologues
        "startTimestamp": 0,
        "endTimestamp": 0,
        "status": "FAILURE",
        "title": "Yo dawg",
        "summary": "Summery"
    }

def test_get_monologue_returns_401_when_not_signed_in(mock_client, auth_mock, monologue_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/monologues/1337"
    )

    # Assert
    monologue_mock.get_user_monologue.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_monologue_returns_404_for_nonexistent_monologue(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    monologue_mock.get_user_monologue.side_effect = NonexistentMonologueError(6000)

    # Act
    res = mock_client.get(
        "/api/monologues/6000"
    )

    # Assert
    monologue_mock.get_user_monologue.assert_called_with(
        user_id=1,
        monologue_id=6000
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_abort_monologue_returns_200_and_aborts_monologue_on_user_request(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.post(
        "/api/monologues/75/abort"
    )

    # Assert
    monologue_mock.end_user_monologue.assert_called_with(
        user_id=1,
        monologue_id=75,
        successful=False
    )
    assert res.status_code == status.HTTP_200_OK

def test_abort_monologue_returns_401_when_not_logged_in(mock_client, auth_mock, monologue_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/monologues/75/abort"
    )

    # Assert
    monologue_mock.end_user_monologue.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_abort_monologue_returns_404_for_nonexistent_monologue(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    monologue_mock.end_user_monologue.side_effect = NonexistentMonologueError(75)

    # Act
    res = mock_client.post(
        "/api/monologues/75/abort"
    )

    # Assert
    monologue_mock.end_user_monologue.assert_called_with(
        user_id=1,
        monologue_id=75,
        successful=False
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_end_monologue_returns_200_and_ends_monologue_on_agent_request(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res_success = mock_client.post(
        "/api/monologues/1/end",
        json={
            "successful": True,
            "reason": "I have my reasons..."
        }
    )

    # Assert
    monologue_mock.end_user_monologue.assert_called_with(
        user_id=1,
        monologue_id=1,
        successful=True
    )
    assert res_success.status_code == status.HTTP_200_OK

    # Act
    res_failure = mock_client.post(
        "/api/monologues/2/end",
        json={
            "successful": False,
            "reason": "I have my reasons..."
        }
    )

    # Assert
    monologue_mock.end_user_monologue.assert_called_with(
        user_id=1,
        monologue_id=2,
        successful=False
    )
    assert res_failure.status_code == status.HTTP_200_OK

def test_end_monologue_returns_401_when_not_logged_in(mock_client, auth_mock, monologue_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/monologues/200/end",
        json={
            "successful": True,
            "reason": "Reason!"
        }
    )

    # Assert
    monologue_mock.end_user_monologue.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_end_monologue_returns_404_for_nonexistent_monologue(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    monologue_mock.end_user_monologue.side_effect = NonexistentMonologueError(200)

    # Act
    res = mock_client.post(
        "/api/monologues/200/end",
        json={
            "successful": True,
            "reason": "Reason!"
        }
    )

    # Assert
    monologue_mock.end_user_monologue.assert_called_with(
        user_id=1,
        monologue_id=200,
        successful=True
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_get_monologue_thoughts_returns_200_and_thoughts_with_formatted_invocations_on_user_request(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    monologue = Monologue(
        id=1337,
        status=MonologueStatus.PENDING,
        agent=Agent(
            id=600
        ),
        event_id=33,
        event=Event(
            id=33
        )
    )
    monologue_mock.get_user_monologue_thoughts.return_value = [
        Thought(
            id=1,
            timestamp=datetime.fromtimestamp(1),
            monologue=monologue,
            invocation=None,
            result="An email has arrived..."
        ),
        Thought(
            id=2,
            timestamp=datetime.fromtimestamp(2),
            monologue=monologue,
            invocation=Invocation(
                function_name="think",
                params={
                    "content": "I should add it to the calendar"
                }
            ),
            result="I should add it to the calendar"
        ),
        Thought(
            id=3, 
            timestamp=datetime.fromtimestamp(3),
            monologue=monologue,
            invocation=Invocation(
                function_name="add_to_calendar",
                params={
                    "event_name": "Conference",
                    "event_timestamp": 20000
                }
            ),
            result="Event successfully added to calendar"
        ),
        Thought(
            id=4,
            timestamp=datetime.fromtimestamp(4),
            monologue=monologue,
            invocation=Invocation(
                function_name="end_monologue",
                params={
                    "successful": True,
                    "reason": "Email processed"
                }
            )
        ),
        Thought(
            id=5,
            timestamp=datetime.fromtimestamp(5),
            monologue=monologue,
            invocation=Invocation(
                function_name="end_monologue",
                params={
                    "successful": False,
                    "reason": "Email processing failed"
                }
            )
        )
    ]

    # Act
    res = mock_client.get(
        "/api/monologues/42/thoughts"
    )

    # Assert
    monologue_mock.get_user_monologue_thoughts.assert_called_with(
        user_id=1,
        monologue_id=42
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "startTimestamp": 1,
            "invocation": {
                "type": "TriggerInvocation",
                "name": None,
                "parameters": {
                    "eventId": 33
                }
            },
            "result": "An email has arrived..."
        },
        {
            "id": 2,
            "startTimestamp": 2,
            "invocation": {
                "type": "ThoughtInvocation",
                "name": None,
                # FIXME: The information in the response is redundant
                "parameters": {
                    "thought": "I should add it to the calendar"
                }
            },
            "result": "I should add it to the calendar"
        },
        {
            "id": 3,
            "startTimestamp": 3,
            "invocation": {
                "type": "ActionInvocation",
                "name": "add_to_calendar",
                "parameters": {
                    "event_name": "Conference",
                    "event_timestamp": 20000
                }
            },
            "result": "Event successfully added to calendar"
        },
        {
            "id": 4,
            "startTimestamp": 4,
            "invocation": {
                "type": "SuccessInvocation",
                "name": None,
                "parameters": { }
            },
            "result": ""
        },
        {
            "id": 5,
            "startTimestamp": 5,
            "invocation": {
                "type": "FailureInvocation",
                "name": None,
                "parameters": { }
            },
            "result": ""
        }
    ]

def test_get_monologue_thoughts_returns_401_when_not_logged_in(mock_client, auth_mock, monologue_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/monologues/13/thoughts"
    )

    # Assert
    monologue_mock.get_user_monologue_thoughts.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_monologue_thoughts_returns_404_for_nonexistent_monologue(mock_client, auth_mock, monologue_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    monologue_mock.get_user_monologue_thoughts.side_effect = NonexistentMonologueError(18)

    # Act
    res = mock_client.get(
        "/api/monologues/18/thoughts"
    )

    # Assert
    monologue_mock.get_user_monologue_thoughts.assert_called_with(
        user_id=1,
        monologue_id=18
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
