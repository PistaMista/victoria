import pytest
from unittest import mock
from app.services.db import DatabaseService
from app.services.agent import AgentService, InvalidAgentSettingError, NonexistentAgentError, AgentDiff
from app.model.user import User, Role
from app.model.agent import Agent
from app.model.action import Action
from app.model.monologue import Monologue, MonologueStatus
from app.model.event import Event
from app.model.trigger import PollTrigger, ChatTrigger
from app.model.action_repository import ActionRepository
from app.model.language_model import LanguageModel
from app.model.llm_connection import OllamaConnection
from sqlalchemy import select

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

def test_agent_service_can_get_all_agents_owned_by_user(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )

    agent_cook = Agent(
        name="Cook",
        prompt="Cook prompt"
    )
    agent_secretary = Agent(
        name="Secretary",
        prompt="Secretary prompt"
    )
    agent_reporter = Agent(
        name="Reporter",
        prompt="Reporter prompt"
    )

    user_john = User(
        id=23,
        username="John",
        password_hash="",
        role=Role.USER,
        agents=[agent_secretary]
    )
    user_tom = User(
        id=30,
        username="Tom",
        password_hash="",
        role=Role.USER,
        agents=[agent_cook, agent_reporter]
    )

    db_session.add(user_john)
    db_session.add(user_tom)
    db_session.commit()

    # Act
    res = serv.get_user_agents(user_id=30)

    # Assert
    assert len(res) == 2
    assert res[0].name == "Cook"
    assert res[0].prompt == "Cook prompt"
    assert res[1].name == "Reporter"
    assert res[1].prompt == "Reporter prompt"

def test_agent_service_returns_empty_list_when_getting_agents_for_nonexistent_user(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )

    agent_cook = Agent(
        name="Cook",
        prompt="Cook prompt"
    )
    agent_secretary = Agent(
        name="Secretary",
        prompt="Secretary prompt"
    )
    agent_reporter = Agent(
        name="Reporter",
        prompt="Reporter prompt"
    )

    user_john = User(
        id=23,
        username="John",
        password_hash="",
        role=Role.USER,
        agents=[agent_secretary]
    )
    user_tom = User(
        id=30,
        username="Tom",
        password_hash="",
        role=Role.USER,
        agents=[agent_cook, agent_reporter]
    )

    db_session.add(user_john)
    db_session.add(user_tom)
    db_session.commit()

    # Act
    res = serv.get_user_agents(user_id=31)

    # Assert
    assert res == []


def test_agent_service_can_find_if_agent_has_any_running_monologues(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )
    trigger = PollTrigger(
        name="Name",
        template="Template",
        url="lol",
        interval=200
    )

    agent_cook = Agent(
        id=12,
        name="Cook",
        prompt="Cook prompt",
        monologues=[
            Monologue(
                title="Get available ingredients",
                status=MonologueStatus.SUCCESS,
                event=Event(
                    trigger=trigger,
                    content="Template",
                    dispatched=True
                )
            ),
            Monologue(
                title="Make recipe",
                status=MonologueStatus.RUNNING,
                event=Event(
                    trigger=trigger,
                    content="Template",
                    dispatched=True
                )
            )
        ]
    )
    agent_reporter = Agent(
        id=33,
        name="Reporter",
        prompt="Reporter prompt",
        monologues=[
            Monologue(
                title="Check world news",
                status=MonologueStatus.PENDING,
                event=Event(
                    trigger=trigger,
                    content="Template",
                    dispatched=True
                )
            )
        ]
    )

    user_tom = User(
        id=30,
        username="Tom",
        password_hash="",
        role=Role.USER,
        agents=[agent_cook, agent_reporter]
    )

    db_session.add(user_tom)
    db_session.commit()

    # Act
    res_cook = serv.is_agent_running_monologues(12)
    res_reporter = serv.is_agent_running_monologues(33)

    assert res_cook == True
    assert res_reporter == False

def test_agent_service_can_create_a_new_agent_with_valid_settings(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action, end_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.commit()

    # Act
    serv.add_user_agent(
        user_id=777,
        name="Mega",
        model_id=12,
        system_prompt="Hello",
        model_parameters={
            "top_k": 0.95,
            "temperature": 1.2
        },
        enabled_trigger_ids=[45],
        enabled_action_ids=[10, 30]
    )

    # Assert
    agent = db_session.scalar(
        select(Agent)
    )

    assert agent is not None
    assert agent.name == "Mega"
    assert agent.model.name == "gemma3:12b"
    assert agent.prompt == "Hello"
    assert agent.model_params == {
        "top_k": 0.95,
        "temperature": 1.2
    }
    assert len(agent.allowed_triggers) == 1
    assert agent.allowed_triggers[0].name == "Poll"
    assert len(agent.allowed_actions) == 2
    assert agent.allowed_actions[0].function_name == "search_web"
    assert agent.allowed_actions[1].function_name == "think"


def test_agent_service_throws_when_creating_agent_for_nonexistent_user(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action, end_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.commit()

    # Act / Assert
    with pytest.raises(InvalidAgentSettingError):
        serv.add_user_agent(
            user_id=1,
            name="Mega",
            model_id=12,
            system_prompt="Hello",
            model_parameters={
                "top_k": 0.95,
                "temperature": 1.2
            },
            enabled_trigger_ids=[45],
            enabled_action_ids=[10, 30]
        )

def test_agent_service_throws_when_creating_agent_with_nonexistent_actions(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action, end_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.commit()

    # Act / Assert
    with pytest.raises(InvalidAgentSettingError):
        serv.add_user_agent(
            user_id=777,
            name="Mega",
            model_id=12,
            system_prompt="Hello",
            model_parameters={
                "top_k": 0.95,
                "temperature": 1.2
            },
            enabled_trigger_ids=[45],
            enabled_action_ids=[10, 11, 30]
        )

def test_agent_service_throws_when_creating_agent_with_nonexistent_triggers(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action, end_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.commit()

    # Act / Assert
    with pytest.raises(InvalidAgentSettingError):
        serv.add_user_agent(
            user_id=777,
            name="Mega",
            model_id=12,
            system_prompt="Hello",
            model_parameters={
                "top_k": 0.95,
                "temperature": 1.2
            },
            enabled_trigger_ids=[47],
            enabled_action_ids=[10, 30]
        )

def test_agent_service_throws_when_creating_agent_with_nonexistent_model(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action, end_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.commit()

    # Act / Assert
    with pytest.raises(InvalidAgentSettingError):
        serv.add_user_agent(
            user_id=777,
            name="Mega",
            model_id=13,
            system_prompt="Hello",
            model_parameters={
                "top_k": 0.95,
                "temperature": 1.2
            },
            enabled_trigger_ids=[45],
            enabled_action_ids=[10, 30]
        )

def test_agent_service_throws_when_creating_agent_with_disallowed_actions(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, end_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.commit()

    # Act
    with pytest.raises(InvalidAgentSettingError):
        serv.add_user_agent(
            user_id=777,
            name="Mega",
            model_id=12,
            system_prompt="Hello",
            model_parameters={
                "top_k": 0.95,
                "temperature": 1.2
            },
            enabled_trigger_ids=[45],
            # "think" action (id 10) is disallowed
            enabled_action_ids=[10, 30]
        )

def test_agent_service_throws_when_creating_agent_with_disallowed_triggers(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )

    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action, end_action],
        allowed_triggers=[]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.commit()

    # Act
    with pytest.raises(InvalidAgentSettingError):
        serv.add_user_agent(
            user_id=777,
            name="Mega",
            model_id=12,
            system_prompt="Hello",
            model_parameters={
                "top_k": 0.95,
                "temperature": 1.2
            },
            # The trigger is disallowed
            enabled_trigger_ids=[45],
            enabled_action_ids=[10, 30]
        )

def test_agent_service_can_get_an_agent_by_id_including_actions_and_triggers(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    res = serv.get_user_agent_by_id(777, 32)

    # Assert
    assert res is not None
    assert res.id == 32
    assert res.name == "Sysadmin"
    assert res.prompt == "You are a thing"
    assert res.owner_id == 777
    assert res.model_id == 12
    assert res.model_params == {
        "lol": 20,
        "foo": 40.2
    }
    assert len(res.allowed_actions) == 2
    assert res.allowed_actions[0].function_name == "search_web"
    assert res.allowed_actions[1].function_name == "think"


def test_agent_service_can_do_simple_agent_update_with_valid_settings(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    new_model = LanguageModel(
        id=19,
        name="llama3.1:8b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model, new_model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    serv.update_user_agent(
        user_id=777,
        agent_id=32,
        diff=AgentDiff(
            name="Cook",
            model_id=19
        )
    )

    # Assert
    db_session.refresh(agent)
    assert agent.name == "Cook"
    assert agent.prompt == "You are a thing"
    assert agent.model.name == "llama3.1:8b"
    assert agent.model_params == {
        "lol": 20,
        "foo": 40.2
    }
    assert len(agent.allowed_actions) == 2
    assert agent.allowed_actions[0].function_name == "search_web"
    assert agent.allowed_actions[1].function_name == "think"
    assert len(agent.allowed_triggers) == 1
    assert agent.allowed_triggers[0].name == "Poll"

def test_agent_service_can_do_complex_agent_update_with_valid_settings(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    new_model = LanguageModel(
        id=19,
        name="llama3.1:8b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model, new_model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )
    new_trigger = ChatTrigger(
        id=66,
        name="Chat",
        template="",
        receiver="general"
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action, end_action],
        allowed_triggers=[trigger, new_trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action, end_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2,
            "temperature": 451.0
        },
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    serv.update_user_agent(
        user_id=777,
        agent_id=32,
        diff=AgentDiff(
            prompt="New!",
            model_params={
                # Unsets the "lol" param
                "lol": None,
                # Updates the "foo" param
                "foo": 37,
                # Adds the "top_k" param
                "top_k": 0.5
            },
            enabled_trigger_ids=[66],
            enabled_action_ids=[30, 20]
        )
    )

    # Assert
    db_session.refresh(agent)
    assert agent.name == "Sysadmin"
    assert agent.prompt == "New!"
    assert agent.model.name == "gemma3:12b"
    assert agent.model_params == {
        "foo": 37,
        "top_k": 0.5,
        "temperature": 451.0
    }
    assert len(agent.allowed_actions) == 2
    assert agent.allowed_actions[0].function_name == "search_web"
    assert agent.allowed_actions[1].function_name == "end_workflow"
    assert len(agent.allowed_triggers) == 1
    assert agent.allowed_triggers[0].name == "Chat"

def test_agent_service_throws_when_updating_agent_with_nonexistent_actions(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    new_model = LanguageModel(
        id=19,
        name="llama3.1:8b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model, new_model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    with pytest.raises(InvalidAgentSettingError):
        serv.update_user_agent(
            user_id=777,
            agent_id=32,
            diff=AgentDiff(
                name="Cook",
                model_id=19,
                enabled_action_ids=[11, 30],
                enabled_trigger_ids=[]
            )
        )

def test_agent_service_throws_when_updating_agent_with_nonexistent_triggers(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    new_model = LanguageModel(
        id=19,
        name="llama3.1:8b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model, new_model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    with pytest.raises(InvalidAgentSettingError):
        serv.update_user_agent(
            user_id=777,
            agent_id=32,
            diff=AgentDiff(
                name="Cook",
                model_id=19,
                enabled_action_ids=[10],
                enabled_trigger_ids=[90]
            )
        )

def test_agent_service_throws_when_updating_agent_with_nonexistent_model(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    new_model = LanguageModel(
        id=19,
        name="llama3.1:8b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model, new_model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[search_action, think_action],
        allowed_triggers=[trigger]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    with pytest.raises(InvalidAgentSettingError):
        serv.update_user_agent(
            user_id=777,
            agent_id=32,
            diff=AgentDiff(
                model_id=983235
            )
        )

def test_agent_service_throws_when_updating_agent_with_disallowed_actions(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    new_model = LanguageModel(
        id=19,
        name="llama3.1:8b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model, new_model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[think_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[think_action],
        allowed_triggers=[trigger]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    with pytest.raises(InvalidAgentSettingError):
        serv.update_user_agent(
            user_id=777,
            agent_id=32,
            diff=AgentDiff(
                enabled_action_ids=[30]
            )
        )

def test_agent_service_throws_when_updating_agent_with_disallowed_triggers(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )


    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    new_model = LanguageModel(
        id=19,
        name="llama3.1:8b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model, new_model]
    )
    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[think_action, search_action],
        allowed_triggers=[]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[think_action],
        allowed_triggers=[]
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.commit()

    # Act
    with pytest.raises(InvalidAgentSettingError):
        serv.update_user_agent(
            user_id=777,
            agent_id=32,
            diff=AgentDiff(
                enabled_action_ids=[30],
                enabled_trigger_ids=[45]
            )
        )

def test_agent_service_can_remove_agent(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )

    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )

    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[think_action, search_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[think_action],
        allowed_triggers=[trigger]
    )

    monologue = Monologue(
        event=Event(
            trigger=trigger,
            content="",
            dispatched=True
        ),
        agent=agent,
        status=MonologueStatus.SUCCESS
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.add(monologue)
    db_session.commit()

    # Act
    serv.remove_user_agent(
        user_id=777,
        agent_id=32
    )

    # Assert
    first_agent = db_session.scalar(
        select(Agent)
    )
    assert first_agent is None
    
    # monologues are removed with the agent
    first_monologue = db_session.scalar(
        select(Monologue)
    )
    assert first_monologue is None

def test_agent_service_throws_when_trying_to_manipulate_nonexistent_agent(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )

    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )

    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[think_action, search_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[think_action],
        allowed_triggers=[trigger]
    )

    monologue = Monologue(
        event=Event(
            trigger=trigger,
            content="",
            dispatched=True
        ),
        agent=agent,
        status=MonologueStatus.SUCCESS
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.add(monologue)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentAgentError):
        serv.is_agent_running_monologues(100)

    with pytest.raises(NonexistentAgentError):
        serv.get_user_agent_by_id(user_id=777, agent_id=100)

    with pytest.raises(NonexistentAgentError):
        serv.update_user_agent(user_id=777, agent_id=100, diff=AgentDiff())

    with pytest.raises(NonexistentAgentError):
        serv.remove_user_agent(user_id=777, agent_id=100)

    with pytest.raises(NonexistentAgentError):
        serv.get_user_agent_monologues(user_id=777, agent_id=100)


def test_agent_service_throws_when_trying_to_manipulate_existing_agent_with_nonexistent_user_id(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )

    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )

    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[think_action, search_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[think_action],
        allowed_triggers=[trigger]
    )

    monologue = Monologue(
        event=Event(
            trigger=trigger,
            content="",
            dispatched=True
        ),
        agent=agent,
        status=MonologueStatus.SUCCESS
    )

    db_session.add(user)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.add(monologue)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentAgentError):
        serv.get_user_agent_by_id(user_id=99999, agent_id=32)

    with pytest.raises(NonexistentAgentError):
        serv.update_user_agent(user_id=99999, agent_id=32, diff=AgentDiff())

    with pytest.raises(NonexistentAgentError):
        serv.remove_user_agent(user_id=99999, agent_id=32)

    with pytest.raises(NonexistentAgentError):
        serv.get_user_agent_monologues(user_id=99999, agent_id=32)

def test_agent_service_throws_when_trying_to_manipulate_existing_agent_with_non_owner(db_serv, db_session):
    # Arrange
    serv = AgentService(
        database_service=db_serv
    )

    model = LanguageModel(
        id=12,
        name="gemma3:12b",
        enabled=True
    )

    connection = OllamaConnection(
        name="Ollama",
        url="golem:11434",
        models=[model]
    )

    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    search_action = Action(
        id=30,
        function_name="search_web",
        function_param_schema={
            "query": "str"
        },
        function_docstring="Searches the web.",
        function_source_code=""
    )

    trigger = PollTrigger(
        id=45,
        name="Poll",
        template="",
        url="seznam.cz",
        interval=200
    )

    user = User(
        id=777,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_actions=[think_action, search_action],
        allowed_triggers=[trigger]
    )

    user_other = User(
        id=1,
        username="Fake",
        password_hash="",
        role=Role.USER,
        allowed_actions=[think_action, search_action],
        allowed_triggers=[trigger]
    )

    action_repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[search_action, think_action]
    )

    agent = Agent(
        id=32,
        name="Sysadmin",
        prompt="You are a thing",
        owner=user,
        model=model,
        model_params={
            "lol": 20,
            "foo": 40.2
        },
        allowed_actions=[think_action],
        allowed_triggers=[trigger]
    )

    monologue = Monologue(
        event=Event(
            trigger=trigger,
            content="",
            dispatched=True
        ),
        agent=agent,
        status=MonologueStatus.SUCCESS
    )

    db_session.add(user)
    db_session.add(user_other)
    db_session.add(action_repo)
    db_session.add(trigger)
    db_session.add(connection)
    db_session.add(agent)
    db_session.add(monologue)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentAgentError):
        serv.get_user_agent_by_id(user_id=1, agent_id=32)

    with pytest.raises(NonexistentAgentError):
        serv.update_user_agent(user_id=1, agent_id=32, diff=AgentDiff())

    with pytest.raises(NonexistentAgentError):
        serv.remove_user_agent(user_id=1, agent_id=32)

    with pytest.raises(NonexistentAgentError):
        serv.get_user_agent_monologues(user_id=1, agent_id=32)
