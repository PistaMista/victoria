import pytest
from unittest import mock
from app.services.monologues import MonologueService, NonexistentMonologueError
from app.services.db import DatabaseService
from app.services.llm import UserMessage, AssistantMessage
from app.model.user import User, Role
from app.model.action import Action
from app.model.agent import Agent
from app.model.monologue import Monologue, MonologueStatus
from app.model.trigger import PollTrigger, TimerTrigger
from app.model.event import Event
from app.model.thought import Thought
from app.model.invocation import Invocation
from app.model.action import Action
from app.model.action_repository import ActionRepository
from datetime import datetime, UTC

@pytest.fixture(scope="function")
def owner():
    return User(
        username="John",
        password_hash="",
        role=Role.USER
    )

@pytest.fixture(scope="function")
def sample_monologue(db_session, owner):
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived...",
        interval=600
    )
    action_repo = ActionRepository(
        name="Default",
        url="https://www.github.com/SOME_ACTION_REPO"
    )
    send_message_action = Action(
        id=390,
        function_name="send_message",
        function_param_schema={},
        function_source_code="",
        function_docstring="",
        repository=action_repo
    )
    think_action = Action(
        id=391,
        function_name="think",
        function_param_schema={},
        function_source_code="",
        function_docstring="",
        repository=action_repo
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
        owner=owner,
        allowed_triggers=[trigger],
        allowed_actions=[think_action, send_message_action]
    )
    event = Event(
        id=42, 
        content="An email has arrived...", 
        trigger=trigger, 
        dispatched=True,
        monologues=[]
    )

    trigger_thought = Thought(
        timestamp=datetime.fromtimestamp(1),
        invocation=None,
        result="An email has arrived..."
    )
    verbatim_invocation = Invocation(
        action=think_action,
        function_name="think",
        params={
            "content": "I should notify the user of the new email"
        }
    )
    verbatim_thought = Thought(
        timestamp=datetime.fromtimestamp(2),
        invocation=verbatim_invocation,
        result="I should notify the user of the new email"
    )
    action_invocation = Invocation(
        action=send_message_action,
        function_name="send_message",
        params={
            "exchange_id": 3,
            "message": "A new email has arrived"
        }
    )
    action_thought = Thought(
        timestamp=datetime.fromtimestamp(3),
        invocation=action_invocation,
        result="Message sent successfully"
    )
    monologue = Monologue(
        id=45,
        title="Handle incoming email",
        summary="Thinking",
        event=event,
        agent=agent,
        status=MonologueStatus.PENDING,
        context={
        },
        thoughts=[
            trigger_thought,
            verbatim_thought,
            action_thought
        ]
    )
    event.monologues = [ monologue ]
    
    db_session.add(monologue)
    db_session.commit()
    
    return monologue

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

def test_monologue_service_can_list_user_monologues(db_serv, db_session):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    trigger = TimerTrigger(
        name="Daily tasks", 
        template="Do your task",
        interval=600
    )
    event = Event(
        id=42, 
        content="Do your task", 
        trigger=trigger, 
        dispatched=True
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="",
        role=Role.USER,
        agents=[
            Agent(
                name="Researcher",
                prompt="",
                monologues=[
                    Monologue(
                        title="Find sources",
                        summary="Searching web for sources...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(10, tz=UTC),
                        event=event
                    ),
                    Monologue(
                        title="Search book notes",
                        summary="Accessing Zettelkasten...",
                        status=MonologueStatus.SUCCESS,
                        modified_at=datetime.fromtimestamp(9, tz=UTC),
                        event=event
                    ),
                    Monologue(
                        title="Prepare plan",
                        summary="Failed to access task list",
                        status=MonologueStatus.FAILURE,
                        modified_at=datetime.fromtimestamp(8, tz=UTC),
                        event=event
                    )
                ]
            ),
            Agent(
                name="Cook",
                prompt="",
                monologues=[
                    Monologue(
                        title="Gather potential recipes",
                        summary="Searching web for recipes...",
                        status=MonologueStatus.SUCCESS,
                        modified_at=datetime.fromtimestamp(7, tz=UTC),
                        event=event
                    ),
                    Monologue(
                        title="Prepare recipes for the week",
                        summary="Exporting recipes to calendar...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(6, tz=UTC),
                        event=event
                    )
                ]
            )
        ]
    )
    user_victor = User(
        id=2,
        username="Victor",
        password_hash="",
        role=Role.USER,
        agents=[
            Agent(
                name="Writer",
                prompt="",
                monologues=[
                    Monologue(
                        title="Write stories",
                        summary="Exporting to Zettelkasten...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(1, tz=UTC),
                        event=event
                    )
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    res_all = service.get_user_monologues(
        user_id=1
    )
    res_running = service.get_user_monologues(
        user_id=1,
        status_filter=MonologueStatus.RUNNING
    )
    res_search = service.get_user_monologues(
        user_id=1,
        search_query="Search"
    )

    # Assert
    # ...results are always sorted by status (RUNNING->PENDING->FINISHED), then by modified_at time (descending)
    assert len(res_all) == 5
    assert res_all[0].title == "Find sources"
    assert res_all[1].title == "Prepare recipes for the week"
    assert res_all[2].title == "Search book notes"
    assert res_all[3].title == "Prepare plan"
    assert res_all[4].title == "Gather potential recipes"

    assert len(res_running) == 2
    assert res_all[0].title == "Find sources"
    assert res_all[1].title == "Prepare recipes for the week"

    assert len(res_search) == 3
    assert res_search[0].title == "Find sources"
    assert res_search[1].title == "Search book notes"
    assert res_search[2].title == "Gather potential recipes"


def test_monologue_service_returns_empty_list_when_listing_monologues_of_nonexistent_user(db_serv, db_session):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    trigger = TimerTrigger(
        name="Daily tasks", 
        template="Do your task",
        interval=600
    )
    event = Event(
        id=42, 
        content="Do your task", 
        trigger=trigger, 
        dispatched=True
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="",
        role=Role.USER,
        agents=[
            Agent(
                name="Researcher",
                prompt="",
                monologues=[
                    Monologue(
                        title="Find sources",
                        summary="Searching web for sources...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(10, tz=UTC),
                        event=event
                    ),
                    Monologue(
                        title="Search book notes",
                        summary="Accessing Zettelkasten...",
                        status=MonologueStatus.SUCCESS,
                        modified_at=datetime.fromtimestamp(9, tz=UTC),
                        event=event
                    ),
                    Monologue(
                        title="Prepare plan",
                        summary="Failed to access task list",
                        status=MonologueStatus.FAILURE,
                        modified_at=datetime.fromtimestamp(8, tz=UTC),
                        event=event
                    )
                ]
            ),
            Agent(
                name="Cook",
                prompt="",
                monologues=[
                    Monologue(
                        title="Gather potential recipes",
                        summary="Searching web for recipes...",
                        status=MonologueStatus.SUCCESS,
                        modified_at=datetime.fromtimestamp(7, tz=UTC),
                        event=event
                    ),
                    Monologue(
                        title="Prepare recipes for the week",
                        summary="Exporting recipes to calendar...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(6, tz=UTC),
                        event=event
                    )
                ]
            )
        ]
    )
    user_victor = User(
        id=2,
        username="Victor",
        password_hash="",
        role=Role.USER,
        agents=[
            Agent(
                name="Writer",
                prompt="",
                monologues=[
                    Monologue(
                        title="Write stories",
                        summary="Exporting to Zettelkasten...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(1, tz=UTC),
                        event=event
                    )
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    res_all = service.get_user_monologues(
        user_id=99
    )
    res_running = service.get_user_monologues(
        user_id=99,
        status_filter=MonologueStatus.RUNNING
    )
    res_search = service.get_user_monologues(
        user_id=99,
        search_query="Search"
    )

    # Assert
    assert res_all == []
    assert res_running == []
    assert res_search == []

def test_monologue_service_can_get_user_monologue_by_id(db_serv, db_session):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    trigger = TimerTrigger(
        name="Daily tasks", 
        template="Do your task",
        interval=600
    )
    event = Event(
        id=42, 
        content="Do your task", 
        trigger=trigger, 
        dispatched=True
    )
    user_john = User(
        id=1,
        username="John",
        password_hash="",
        role=Role.USER,
        agents=[
            Agent(
                name="Researcher",
                prompt="",
                monologues=[
                    Monologue(
                        id=1,
                        title="Find sources",
                        summary="Searching web for sources...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(10, tz=UTC),
                        event=event
                    ),
                    Monologue(
                        id=2,
                        title="Prepare plan",
                        summary="Failed to access task list",
                        status=MonologueStatus.FAILURE,
                        modified_at=datetime.fromtimestamp(8, tz=UTC),
                        event=event
                    )
                ]
            ),
            Agent(
                name="Cook",
                prompt="",
                monologues=[
                    Monologue(
                        id=3,
                        title="Gather potential recipes",
                        summary="Searching web for recipes...",
                        status=MonologueStatus.SUCCESS,
                        modified_at=datetime.fromtimestamp(7, tz=UTC),
                        event=event
                    )
                ]
            )
        ]
    )
    user_victor = User(
        id=2,
        username="Victor",
        password_hash="",
        role=Role.USER,
        agents=[
            Agent(
                name="Writer",
                prompt="",
                monologues=[
                    Monologue(
                        id=4,
                        title="Write stories",
                        summary="Exporting to Zettelkasten...",
                        status=MonologueStatus.RUNNING,
                        modified_at=datetime.fromtimestamp(1, tz=UTC),
                        event=event
                    )
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    res = service.get_user_monologue(user_id=2, monologue_id=4)

    # Assert
    assert isinstance(res, Monologue)
    assert res.id == 4
    assert res.title == "Write stories"
    assert res.summary == "Exporting to Zettelkasten..."
    assert res.status == MonologueStatus.RUNNING

@mock.patch("app.services.monologues.MonologueService.set_monologue_status")
def test_monologue_service_can_end_user_monologue_with_success(mock_set_status, sample_monologue, db_serv):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )

    # Act
    service.end_user_monologue(sample_monologue.agent.owner_id, sample_monologue.id, True)

    # Assert
    mock_set_status.assert_called_once_with(id=sample_monologue.id, status=MonologueStatus.SUCCESS)

@mock.patch("app.services.monologues.MonologueService.set_monologue_status")
def test_monologue_service_can_end_user_monologue_with_failure(mock_set_status, sample_monologue, db_serv):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )

    # Act
    service.end_user_monologue(sample_monologue.agent.owner_id, sample_monologue.id, False)

    # Assert
    mock_set_status.assert_called_once_with(id=sample_monologue.id, status=MonologueStatus.FAILURE)



def test_monologue_service_can_get_user_monologue_thoughts_including_invocations(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )

    # Act
    res = service.get_user_monologue_thoughts(
        user_id=sample_monologue.agent.owner.id, 
        monologue_id=sample_monologue.id
    )

    # Assert
    assert len(res) == 3
    assert res[0].invocation is None
    assert res[0].result == "An email has arrived..."
    assert res[1].invocation.function_name == "think"
    assert res[1].invocation.params == {
        "content": "I should notify the user of the new email"
    }
    assert res[1].result == "I should notify the user of the new email"
    assert res[2].invocation.function_name == "send_message"
    assert res[2].invocation.params == {
        "exchange_id": 3,
        "message": "A new email has arrived"
    }
    assert res[2].result == "Message sent successfully"

def test_monologue_service_can_change_monologue_status(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    
    # Act
    service.set_monologue_status(sample_monologue.id, MonologueStatus.FAILURE)
    
    # Assert
    db_session.refresh(sample_monologue)
    assert sample_monologue.status == MonologueStatus.FAILURE

def test_monologue_service_sets_context_FINISHED_when_changing_monologue_status_to_success(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    
    # Act
    service.set_monologue_status(sample_monologue.id, MonologueStatus.SUCCESS)
    
    # Assert
    db_session.refresh(sample_monologue)
    assert sample_monologue.context["FINISHED"]

def test_monologue_service_sets_context_FINISHED_when_changing_monologue_status_to_failure(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    
    # Act
    service.set_monologue_status(sample_monologue.id, MonologueStatus.FAILURE)
    
    # Assert
    db_session.refresh(sample_monologue)
    assert sample_monologue.context["FINISHED"]

def test_monologue_service_unsets_context_FINISHED_when_changing_monologue_status_to_pending(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    
    # Act
    service.set_monologue_status(sample_monologue.id, MonologueStatus.PENDING)
    
    # Assert
    db_session.refresh(sample_monologue)
    assert not sample_monologue.context["FINISHED"]

def test_monologue_service_unsets_context_FINISHED_when_changing_monologue_status_to_running(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    
    # Act
    service.set_monologue_status(sample_monologue.id, MonologueStatus.RUNNING)
    
    # Assert
    db_session.refresh(sample_monologue)
    assert not sample_monologue.context["FINISHED"]

def test_monologue_service_can_change_monologue_title(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )
    
    # Act
    service.set_monologue_title(sample_monologue.id, "FOR THOSE WHO COME AFTER!")
    
    # Assert
    db_session.refresh(sample_monologue)
    assert sample_monologue.title == "FOR THOSE WHO COME AFTER!"

def test_monologue_service_can_change_monologue_summary(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )
    
    # Act
    service.set_monologue_summary(sample_monologue.id, "summarized something")
    
    # Assert
    db_session.refresh(sample_monologue)
    assert sample_monologue.summary == "summarized something"

def test_monologue_service_can_set_monologue_context(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )

    # Act
    service.set_monologue_context(sample_monologue.id, { "mykey": "myval", "num": 42 })

    # Assert
    db_session.refresh(sample_monologue)
    assert sample_monologue.context == { "mykey": "myval", "num": 42 }
    
def test_monologue_service_can_get_monologue_thoughts(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )
    
    # Act
    res = service.get_monologue_thoughts(sample_monologue.id)
    
    # Assert
    assert len(res) == 3
    assert res[0].invocation is None
    assert res[0].result == "An email has arrived..."
    
    assert res[1].invocation.action.function_name == "think"
    assert res[1].invocation.params["content"] == "I should notify the user of the new email"
    assert res[1].result == "I should notify the user of the new email"
    
    assert res[2].invocation.action.function_name == "send_message"
    assert res[2].invocation.params["exchange_id"] == 3
    assert res[2].invocation.params["message"] == "A new email has arrived"
    assert res[2].result == "Message sent successfully"
    

def test_monologue_service_can_get_monologue_thoughts_as_llm_chat_history(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )
    
    # Act
    res = service.get_monologue_thoughts_as_llm_chat_history(sample_monologue.id)

    # Assert
    assert res == [
        # NOTE: this list does not involve the system prompt
        UserMessage("An email has arrived..."),
        AssistantMessage('{"action_name": "think", "arguments": {"content": "I should notify the user of the new email"}}'),
        UserMessage("I should notify the user of the new email"),
        AssistantMessage('{"action_name": "send_message", "arguments": {"exchange_id": 3, "message": "A new email has arrived"}}'),
        UserMessage("Message sent successfully")
        # NOTE: whether success or failure thoughts appear in the chat history is undefined
    ]

# NOTE: Shouldn't this be done by an agent service? No, since there are monologue specific things which affect which
# actions can be taken.
def test_monologue_service_can_get_monologue_system_prompt(db_serv, db_session, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    send_desc = """send_message:
A VERY INFORMATIVE TOOL DESCRIPTION!"""
    think_desc = """think:
ANOTHER INFORMATIVE TOOL DESCRIPTION"""
    mock_action_serv.get_action_description.side_effect = lambda id: {
        390: send_desc,
        391: think_desc
    }.get(id)
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )
    
    # Act
    res = service.get_monologue_system_prompt(sample_monologue.id)
    
    # Assert
    assert "Manage the user's calendar and tasks" in res
    assert send_desc in res
    assert think_desc in res

def test_monologue_service_can_get_monologue_details(db_serv, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )
    
    # Act
    res = service.get_monologue_by_id(sample_monologue.id)

    # Assert
    assert res.title == sample_monologue.title
    assert res.summary == sample_monologue.summary
    assert res.status == sample_monologue.status

def test_monologue_service_can_get_monologue_agent_id(db_serv, sample_monologue):
    # Arrange
    mock_action_serv = mock.MagicMock()
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )

    # Act
    res = service.get_monologue_agent_id(sample_monologue.id)

    # Assert
    assert res == 75
    

@mock.patch("app.services.monologues.datetime")
def test_monologue_service_can_append_thought_to_monologue(mock_datetime, db_serv, db_session, sample_monologue):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(120, tz=UTC)
    mock_action_serv = mock.MagicMock()    
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv
    )
    action = Action(
        function_name="mega_func",
        function_param_schema={},
        function_source_code="",
        function_docstring="",
        repository=sample_monologue.thoughts[2].invocation.action.repository
    )
    invocation = Invocation(
        action=action,
        function_name="mega_func",
        params={
            "the_mega_param": "foobar"
        }
    )
    thought = Thought(
        timestamp=datetime.fromtimestamp(50),
        invocation=invocation,
        result="Suboptimal"
    )
    
    db_session.add(action)
    db_session.commit()
    
    # NOTE: The objects associated to the Thought must not be attached to any other session
    db_session.expunge(action)
    
    # Act
    service.append_thought_to_monologue(sample_monologue.id, thought)
    
    # Assert
    db_session.refresh(sample_monologue)
    assert sample_monologue.thoughts[3].invocation.action.function_name == "mega_func"
    assert sample_monologue.thoughts[3].invocation.params["the_mega_param"] == "foobar"
    assert sample_monologue.thoughts[3].result == "Suboptimal"
    assert sample_monologue.thoughts[3].timestamp == datetime.fromtimestamp(50)
    # The current time is taken to be the modified_at time, not the timestamp of the added thought
    assert sample_monologue.modified_at == datetime.fromtimestamp(120, tz=UTC)

    
    
def test_monologue_service_throws_when_manipulating_nonexistent_monologue(db_serv, db_session, sample_monologue):
    # Arrange
    non_owner = User(
        username="Victor",
        password_hash="",
        role=Role.USER
    )
    db_session.add(non_owner)
    db_session.commit()

    thought = Thought(
        timestamp=datetime.fromtimestamp(1),
        invocation=None,
        result="An email has arrived..."
    )

    non_owner_id = non_owner.id
    owner_id = sample_monologue.agent.owner.id
    mock_action_serv = mock.MagicMock()
    mock_action_serv.get_tool_description.return_value = """
    send_message:
    A VERY INFORMATIVE TOOL DESCRIPTION
    """
    service = MonologueService(
        database_service=db_serv,
        action_service=mock_action_serv        
    )

    # Act / Assert
    with pytest.raises(NonexistentMonologueError):
        service.get_monologue_thoughts(99)

    with pytest.raises(NonexistentMonologueError):
        service.get_monologue_thoughts_as_llm_chat_history(99)

    with pytest.raises(NonexistentMonologueError):
        service.get_monologue_system_prompt(99)

    with pytest.raises(NonexistentMonologueError):
        service.set_monologue_status(99, MonologueStatus.PENDING)

    with pytest.raises(NonexistentMonologueError):
        service.set_monologue_title(99, "")

    with pytest.raises(NonexistentMonologueError):
        service.set_monologue_summary(99, "")

    with pytest.raises(NonexistentMonologueError):
        service.get_monologue_by_id(99)
    
    with pytest.raises(NonexistentMonologueError):
        service.append_thought_to_monologue(99, thought)

    with pytest.raises(NonexistentMonologueError):
        service.get_monologue_agent_id(99)

    with pytest.raises(NonexistentMonologueError):
        service.get_user_monologue(
            user_id=owner_id,
            monologue_id=99 # Nonexistent
        )

    with pytest.raises(NonexistentMonologueError):
        service.get_user_monologue(
            user_id=99999999, # Nonexistent
            monologue_id=sample_monologue.id 
        )

    with pytest.raises(NonexistentMonologueError):
        service.get_user_monologue(
            user_id=non_owner_id, # Not owner
            monologue_id=sample_monologue.id 
        )

    with pytest.raises(NonexistentMonologueError):
        service.end_user_monologue(
            user_id=owner_id,
            monologue_id=99, # Nonexistent
            successful=False
        )

    with pytest.raises(NonexistentMonologueError):
        service.end_user_monologue(
            user_id=99999999, # Nonexistent
            monologue_id=sample_monologue.id,
            successful=False
        )

    with pytest.raises(NonexistentMonologueError):
        service.end_user_monologue(
            user_id=non_owner_id, # Not owner
            monologue_id=sample_monologue.id,
            successful=False
        )

    with pytest.raises(NonexistentMonologueError):
        service.get_user_monologue_thoughts(
            user_id=owner_id,
            monologue_id=99 # Nonexistent
        )

    with pytest.raises(NonexistentMonologueError):
        service.get_user_monologue_thoughts(
            user_id=99999999, # Nonexistent
            monologue_id=sample_monologue.id 
        )

    with pytest.raises(NonexistentMonologueError):
        service.get_user_monologue_thoughts(
            user_id=non_owner_id, # Not owner
            monologue_id=sample_monologue.id 
        )
