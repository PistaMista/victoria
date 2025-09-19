from app.model.agent import Agent
from app.model.language_model import LanguageModel
from app.model.action import Action
from app.model.trigger import ChatTrigger
from app.services.auth import NotLoggedInError
from app.services.agent import NonexistentAgentError, InvalidAgentSettingError, AgentDiff
from app.services.monologues import Monologue, MonologueStatus
from fastapi import status

def test_list_agents_returns_200_and_list_of_agents_of_current_user_on_valid_request(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    agent_mock.is_agent_running_monologues.side_effect = lambda id: {
            1: True,
            2: False,
            3: True
    }.get(id)
    agent_mock.get_user_agents.return_value = [
        Agent(
            id=1,
            name="Cook"
        ),
        Agent(
            id=2,
            name="Researcher"
        ),
        Agent(
            id=3,
            name="Maintainer"
        )
    ]

    # Act
    res = mock_client.get(
        '/api/agents',
        cookies={"token": "tok"}
    )

    # Assert
    agent_mock.get_user_agents.assert_called_with(1)
    agent_mock.is_agent_running_monologues.assert_any_call(1)
    agent_mock.is_agent_running_monologues.assert_any_call(2)
    agent_mock.is_agent_running_monologues.assert_any_call(3)

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "name": "Cook",
            "status": "BUSY"
        },
        {
            "id": 2,
            "name": "Researcher",
            "status": "IDLE"
        },
        {
            "id": 3,
            "name": "Maintainer",
            "status": "BUSY"
        }
    ]


def test_list_agents_returns_401_when_not_signed_in(mock_client, auth_mock, agent_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/agents',
        cookies={ "token": "tok" }
    )

    # Assert
    agent_mock.is_agent_running_monologues.assert_not_called()
    agent_mock.get_user_agents.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_agent_returns_200_and_creates_agent_for_current_user_on_valid_request(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.post(
        '/api/agents',
        json={
            "name": "John",
            "baseModelId": 3,
            "systemPrompt": "You do things",
            "modelParameters": {
                "temperature": 0.7,
                "top_k": 0.95
            },
            "enabledTriggers": [1, 2, 3],
            "enabledActions": [42]
        },
        cookies={ "token": "tok" }
    )

    # Assert
    agent_mock.add_agent.assert_called_with(
        name="John",
        model_id=3,
        system_prompt="You do things",
        model_parameters={
            "temperature": 0.7,
            "top_k": 0.95
        },
        enabled_trigger_ids=[1, 2, 3],
        enabled_actions=[42]
    )
    assert res.status_code == status.HTTP_200_OK
    


def test_create_agent_returns_401_when_not_signed_in(mock_client, auth_mock, agent_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        '/api/agents',
        json={
            "name": "John",
            "baseModelId": 3,
            "systemPrompt": "You do things",
            "modelParameters": {
                "temperature": 0.7,
                "top_k": 0.95
            },
            "enabledTriggers": [1, 2, 3],
            "enabledActions": [42]
        },
        cookies={ "token": "tok" }
    )

    # Assert
    agent_mock.add_agent.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_agent_returns_200_and_agent_on_valid_request(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    agent_mock.get_user_agent_by_id.return_value = Agent(
        id=42,
        name="Researcher",
        prompt="You research things",
        model=LanguageModel(
            id=20,
            name="gemma3:12b",
            enabled=True
        ),
        model_params={
            "temperature": 0.69,
            "top_k": 4.20,
            "num_gpu": 37
        },
        allowed_triggers=[
            ChatTrigger(
                id=1,
                name="Lol",
                template="lol"
            ),
            ChatTrigger(
                id=2,
                name="Chat2",
                template="weeeee"
            )
        ],
        allowed_actions=[
            Action(
                id=30,
                function_name="tinker",
                function_param_schema={},
                function_source_code="",
                function_docstring="help"
            )
        ]
    )

    # Act
    res = mock_client.get(
        '/api/agents/42',
        cookies={"token": "tok"}
    )

    # Assert
    agent_mock.get_user_agent_by_id.assert_called_with(
        user_id=1,
        agent_id=42
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 42,
        "name": "Researcher",
        "status": "IDLE",
        "baseModelId": 20,
        "systemPrompt": "You research things",
        "modelParameters": {
            "temperature": 0.69,
            "top_k": 4.20,
            "num_gpu": 37
        },
        "enabledTriggers": [1, 2],
        "enabledActions": [30]
    }


def test_get_agent_returns_401_when_not_signed_in(mock_client, auth_mock, agent_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/agents/42',
        cookies={"token": "tok"}
    )

    # Assert
    agent_mock.get_user_agent_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_agent_returns_404_for_nonexistent_agent(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    agent_mock.get_user_agent_by_id.side_effect = NonexistentAgentError(42)

    # Act
    res = mock_client.get(
        '/api/agents/42',
        cookies={"token": "tok"}
    )

    # Assert
    agent_mock.assert_called_with.get_user_agent_by_id(
        user_id=1,
        agent_id=42
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_update_agent_returns_200_and_updates_agent_on_simple_request(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.put(
        '/api/agents/3',
        json={
            "name": "New",
            "baseModelId": 8
        }
    )

    # Assert
    agent_mock.update_user_agent.assert_called_with(
        user_id=1,
        agent_id=3,
        diff=AgentDiff(
            name="New",
            model_id=8
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_update_agent_returns_200_and_updates_agent_on_complex_request(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user

    # Act
    res = mock_client.put(
        '/api/agents/3',
        json={
            "name": "New",
            "baseModelId": 8,
            "modelParameters": {
                "LOLOL": 420,
                "top_dog": 1337
            },
            "enabledTriggers": [7, 6, 4],
            "enabledActions": [42]
        }
    )

    # Assert
    agent_mock.update_user_agent.assert_called_with(
        user_id=1,
        agent_id=3,
        diff=AgentDiff(
            name="New",
            model_id=8,
            model_params={
                "LOLOL": 420,
                "top_dog": 1337
            },
            enabled_trigger_ids=[7, 6, 4],
            enabled_action_ids=[42]
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_update_agent_returns_400_when_using_undefined_ids(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    agent_mock.update_user_agent.side_effect = InvalidAgentSettingError("")

    # Act
    res = mock_client.put(
        '/api/agents/3',
        json={
            "name": "New",
            "baseModelId": 8,
            "modelParameters": {
                "LOLOL": 420,
                "top_dog": 1337
            }
        }
    )

    # Assert
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_update_agent_returns_401_when_not_signed_in(mock_client, auth_mock, agent_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()


    # Act
    res = mock_client.put(
        '/api/agents/3',
        json={
            "name": "New",
            "baseModelId": 8,
            "modelParameters": {
                "LOLOL": 420,
                "top_dog": 1337
            }
        }
    )

    # Assert
    agent_mock.update_user_agent.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_agent_returns_404_for_nonexistent_agent(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    agent_mock.update_user_agent.side_effect = NonexistentAgentError(3)

    # Act
    res = mock_client.put(
        '/api/agents/3',
        json={}
    )

    # Assert
    agent_mock.update_user_agent.assert_called_with(
        user_id=1,
        agent_id=3,
        diff=AgentDiff()
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_list_agent_monologues_returns_200_and_monologue_list_on_valid_request(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    agent_mock.get_user_agent_monologues.return_value = [
        Monologue(
            id=1,
            title="Find ingredients",
            summary="Searching tesco.cz for ingredients",
            status=MonologueStatus.PENDING,
            agent_id=5
        ),
        Monologue(
            id=2,
            title="Order ingredients",
            summary="Executing order on rohlik.cz",
            status=MonologueStatus.RUNNING,
            agent_id=10
        )
    ]

    # Act
    res = mock_client.get(
        '/api/agents/3/monologues',
        cookies={"token": "tok"}
    )

    # Assert
    agent_mock.get_user_agent_monologues.assert_called_with(
        user_id=1,
        agent_id=3
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        # TODO: Add start/end timestamps to Monologues (not yet implemented)
        {
            "id": 1,
            "agentId": 5,
            "startTimestamp": 0,
            "title": "Find ingredients",
            "summary": "Searching tesco.cz for ingredients",
            "status": "PENDING"
        },
        {
            "id": 2,
            "agentId": 10,
            "startTimestamp": 0,
            "title": "Order ingredients",
            "summary": "Executing order on rohlik.cz",
            "status": "RUNNING"
        }
    ]


def test_list_agent_monologues_returns_401_when_not_signed_in(mock_client, auth_mock, agent_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        '/api/agents/3/monologues',
        cookies={"token": "tok"}
    )

    # Assert
    agent_mock.get_user_agent_monologues.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_agent_monologues_returns_404_for_nonexistent_agent(mock_client, auth_mock, agent_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    agent_mock.get_user_agent_monologues.side_effect = NonexistentAgentError(3)

    # Act
    res = mock_client.get(
        '/api/agents/3/monologues',
        cookies={"token": "tok"}
    )

    # Assert
    agent_mock.get_user_agent_monologues.assert_called_with(
        user_id=1,
        agent_id=3
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
