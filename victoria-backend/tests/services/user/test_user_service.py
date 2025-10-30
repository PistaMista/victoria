from app.services.user import UserService, UserDiff, UserExistsError, InvalidUserSettingError, NonexistentUserError
from app.services.db import DatabaseService
from sqlalchemy import select
from app.model.user import User, Role
from app.model.agent import Agent
from app.model.action import Action
from app.model.action_repository import ActionRepository
from app.model.trigger import ChatTrigger, PollTrigger
from app.model.monologue import Monologue, MonologueStatus
from app.model.event import Event
import pytest
from unittest import mock

@pytest.fixture(scope="function")
def serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield UserService(db_service=db)

def test_user_service_can_get_all_registered_users(serv, db_session):
    # Arrange
    user_john = User(
        id=1,
        username="John",
        password_hash="",
        role=Role.USER
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER
    )
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    res = serv.get_all_users()

    # Assert
    assert len(res) == 2
    assert isinstance(res[0], User)
    assert res[0].username == "John"
    assert isinstance(res[1], User)
    assert res[1].username == "Mark"

def test_user_service_can_get_user_of_valid_agent_token(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary]
    )
    monologue = Monologue(
        status=MonologueStatus.RUNNING,
        agent=agent_secretary,
        event=Event(
            dispatched=True,
            trigger=poll_trigger,
            content="Wooo"
        ),
        agent_token=b'abcd'
    )

    db_session.add(poll_trigger)
    db_session.add(user_john)
    db_session.add(monologue)
    db_session.commit()

    # Act
    res = serv.get_user_by_running_monologue_agent_token(b'abcd')

    # Assert
    assert res.id == 1
    assert res.username == "John"

def test_user_service_throws_when_getting_user_of_nonexistent_agent_token(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary]
    )
    monologue = Monologue(
        status=MonologueStatus.RUNNING,
        agent=agent_secretary,
        event=Event(
            dispatched=True,
            trigger=poll_trigger,
            content="Wooo"
        ),
        agent_token=b'abcd'
    )

    db_session.add(poll_trigger)
    db_session.add(user_john)
    db_session.add(monologue)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentUserError):
        serv.get_user_by_running_monologue_agent_token(b'FFFF')


def test_user_service_throws_when_getting_user_of_agent_token_with_finished_monologue(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary]
    )
    monologue = Monologue(
        status=MonologueStatus.FAILURE,
        agent=agent_secretary,
        event=Event(
            dispatched=True,
            trigger=poll_trigger,
            content="Wooo"
        ),
        agent_token=b'abcd'
    )

    db_session.add(poll_trigger)
    db_session.add(user_john)
    db_session.add(monologue)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentUserError):
        serv.get_user_by_running_monologue_agent_token(b'abcd')

def test_user_service_can_update_user_simple(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    serv.update_user(
        id=1,
        changes=UserDiff(
            username="Claudia",
            role=Role.ADMIN
        )
    )


    # Assert
    db_session.refresh(user_john)
    assert user_john.username == "Claudia"
    assert user_john.password_hash == "old"
    assert user_john.role == Role.ADMIN
    assert len(user_john.agents) == 1
    assert user_john.agents[0].id == 75
    assert len(user_john.allowed_triggers) == 1
    assert user_john.allowed_triggers[0].id == 5
    assert len(user_john.allowed_actions) == 2
    assert user_john.allowed_actions[0].id == 391
    assert user_john.allowed_actions[1].id == 390

def test_user_service_can_update_user_complex(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    serv.update_user(
        id=1,
        changes=UserDiff(
            username="New",
            permitted_action_ids=[391],
            permitted_trigger_ids=[5, 10]
        )
    )

    # Assert
    db_session.refresh(user_john)
    assert user_john.username == "New"
    assert user_john.password_hash == "old"
    assert user_john.role == Role.USER
    assert len(user_john.agents) == 1
    assert user_john.agents[0].id == 75
    assert len(user_john.allowed_triggers) == 2
    assert user_john.allowed_triggers[1].id == 5
    assert user_john.allowed_triggers[1].name == "Simple poll"
    assert user_john.allowed_triggers[0].id == 10
    assert user_john.allowed_triggers[0].name == "Simple chat"
    assert len(user_john.allowed_actions) == 1
    assert user_john.allowed_actions[0].id == 391
    assert user_john.allowed_actions[0].function_name == "think"

def test_user_service_can_update_user_password(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    serv.update_user(
        id=1,
        changes=UserDiff(
            new_password="woohoo420"
        )
    )

    # Assert
    db_session.refresh(user_john)
    assert user_john.password_hash != "old"


def test_user_service_newly_permitted_user_triggers_are_NOT_automatically_allowed_to_their_agents(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    serv.update_user(
        id=1,
        changes=UserDiff(
            username="New",
            permitted_action_ids=[391],
            permitted_trigger_ids=[5, 10]
        )
    )

    # Assert
    db_session.refresh(agent_secretary)
    assert len(agent_secretary.allowed_triggers) == 1
    assert agent_secretary.allowed_triggers[0].id == 5
    assert agent_secretary.allowed_triggers[0].name == "Simple poll"


def test_user_service_newly_forbidden_user_triggers_are_disallowed_to_their_agents(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    serv.update_user(
        id=1,
        changes=UserDiff(
            username="New",
            permitted_action_ids=[391],
            permitted_trigger_ids=[10]
        )
    )

    # Assert
    db_session.refresh(agent_secretary)
    assert agent_secretary.allowed_triggers == []


def test_user_service_newly_permitted_user_actions_are_NOT_automatically_allowed_to_their_agents(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    serv.update_user(
        id=1,
        changes=UserDiff(
            username="New",
            permitted_action_ids=[390, 391],
            permitted_trigger_ids=[10]
        )
    )

    # Assert
    db_session.refresh(agent_secretary)
    assert len(agent_secretary.allowed_actions) == 1
    assert agent_secretary.allowed_actions[0].id == 391
    assert agent_secretary.allowed_actions[0].function_name == "think"

def test_user_service_newly_forbidden_user_actions_are_disallowed_to_their_agents(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act
    serv.update_user(
        id=1,
        changes=UserDiff(
            username="New",
            permitted_action_ids=[391],
            permitted_trigger_ids=[10]
        )
    )

    # Assert
    db_session.refresh(agent_secretary)
    assert len(agent_secretary.allowed_actions) == 1
    assert agent_secretary.allowed_actions[0].id == 391
    assert agent_secretary.allowed_actions[0].function_name == "think"

def test_user_service_throws_when_specifying_invalid_ids_for_permitted_actions_and_triggers(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=10,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=20,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act / Assert
    with pytest.raises(InvalidUserSettingError):
        serv.create_user(
            username="askjdnajksdn",
            password="hello",
            role=Role.USER,
            permitted_action_ids=[50], # Nonexistent
            permitted_trigger_ids=[5]
        )

    with pytest.raises(InvalidUserSettingError):
        serv.create_user(
            username="aijsndujqawniu",
            password="hello",
            role=Role.USER,
            permitted_action_ids=[390, 391], 
            permitted_trigger_ids=[6] # Nonexistent
        )

    with pytest.raises(InvalidUserSettingError):
        serv.update_user(
            id=10,
            changes=UserDiff(
                username="New",
                permitted_action_ids=[391, 999999], # Nonexistent
                permitted_trigger_ids=[10]
            )
        )

    with pytest.raises(InvalidUserSettingError):
        serv.update_user(
            id=10,
            changes=UserDiff(
                username="New",
                permitted_action_ids=[391], 
                permitted_trigger_ids=[10, 999999, 15] # Nonexistent
            )
        )

def test_user_service_creates_user_without_permitted_actions_or_triggers(serv, db_session):
    # Arrange
    
    # Act
    new_id = serv.create_user(
        username="John",
        password="hello",
        role=Role.USER,
    )
    
    # Assert
    user = db_session.scalars(
        select(User).where(User.id == new_id)
    ).first()

    assert user is not None
    assert user.username == "John"
    assert user.role == Role.USER
    assert user.allowed_triggers == []
    assert user.allowed_actions == []

def test_user_service_creates_user_with_permitted_actions_and_triggers(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    db_session.add(gitea_repo)
    db_session.add(poll_trigger)
    db_session.add(chat_trigger)
    db_session.commit()
    
    # Act
    new_id = serv.create_user(
        username="John",
        password="hello",
        role=Role.USER,
        permitted_trigger_ids=[5],
        permitted_action_ids=[390, 391]
    )
    
    # Assert
    user = db_session.scalars(
        select(User).where(User.id == new_id)
    ).first()

    assert user is not None
    assert user.username == "John"
    assert user.role == Role.USER
    assert len(user.allowed_triggers) == 1
    assert user.allowed_triggers[0].name == "Simple poll"
    assert len(user.allowed_actions) == 2
    assert user.allowed_actions[0].function_name == "send_message"
    assert user.allowed_actions[1].function_name == "think"

def test_user_service_creates_admin_user(serv, db_session):
    # Arrange
    
    # Act
    serv.create_user(
        username="John",
        password="hello",
        role=Role.ADMIN
    )
    
    # Assert
    user = db_session.scalars(
        select(User).where(User.username == "John")
    ).first()

    assert user is not None
    assert user.username == "John"
    assert user.role == Role.ADMIN

def test_user_service_throws_exception_when_creating_user_with_taken_username(serv, db_session):
    # Arrange
    existing_user = User(
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    with pytest.raises(UserExistsError):
        serv.create_user(
            username="exists",
            password="asdadkjanskjdn",
            role = Role.USER
        )
    
    with pytest.raises(UserExistsError):
        serv.create_user(
            username="exists",
            password="asndkanskjdn",
            role = Role.ADMIN
        )

def test_user_service_reports_when_no_users_are_registered(serv, db_factory):
    # Arrange
    
    # Act / Assert
    assert not serv.is_any_user_registered()
    
def test_user_service_reports_when_any_user_is_registered(serv, db_session):
    # Arrange
    existing_user = User(
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    assert serv.is_any_user_registered()

def test_user_service_gets_user_by_id(serv, db_session, db_factory):
    # Arrange
    existing_user = User(
        id=1,
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    user = serv.get_user_by_id(1)
    assert user.username == "exists"
    assert user.password_hash == "dasdasdasd"
    assert user.role == Role.ADMIN

def test_user_service_gets_user_by_name(serv, db_session, db_factory):
    # Arrange
    existing_user = User(
        id=1,
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    user = serv.get_user_by_name("exists")
    assert user.username == "exists"
    assert user.password_hash == "dasdasdasd"
    assert user.role == Role.ADMIN


def test_user_service_deletes_user(db_session, serv):
    # Arrange
    existing_user = User(
        id=1,
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act
    serv.delete_user_by_id(1)
    
    # Assert
    first_user = db_session.scalars(
        select(User)
    ).first()
    
    assert first_user is None
    assert not serv.is_any_user_registered()

def test_user_service_throws_when_trying_to_manipulate_nonexistent_user(serv, db_session):
    # Arrange
    poll_trigger = PollTrigger(
        id=5,
        name="Simple poll",
        url="seznam.cz",
        template="Content of the website: $(content)",
        interval=30
    )
    chat_trigger = ChatTrigger(
        id=10,
        name="Simple chat",
        receiver="general",
        template="Hello"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring=""
    )
    gitea_repo = ActionRepository(
        name="Gitea",
        url="golem:8080",
        actions=[send_message_action, think_action]
    )
    agent_secretary = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="old",
        role=Role.USER,
        agents=[agent_secretary],
        allowed_triggers=[poll_trigger],
        allowed_actions=[think_action, send_message_action]
    )
    user_mark = User(
        id=2,
        username="Mark",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[chat_trigger],
        allowed_actions=[think_action]
    )
    db_session.add(chat_trigger)
    db_session.add(poll_trigger)
    db_session.add(gitea_repo)
    db_session.add(user_john)
    db_session.add(user_mark)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentUserError):
        serv.delete_user_by_id(id=99999)

    with pytest.raises(NonexistentUserError):
        serv.get_user_by_id(id=99999)

    with pytest.raises(NonexistentUserError):
        serv.get_user_by_name(username="awdbajsd")

    with pytest.raises(NonexistentUserError):
        serv.update_user(id=99999, changes=UserDiff())

