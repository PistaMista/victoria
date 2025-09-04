import pytest
from unittest import mock
from app.services.monologues import MonologueService, NonexistentMonologueError
from app.services.db import DatabaseService
from app.services.llm import UserMessage, AssistantMessage
from app.model.action import Action
from app.model.agent import Agent
from app.model.monologue import Monologue, MonologueStatus
from app.model.trigger import PollTrigger
from app.model.event import Event
from app.model.thought import Thought
from app.model.invocation import Invocation
from app.model.action import Action
from datetime import datetime

@pytest.fixture(scope="function")
def sample_monologue(db_session):
    trigger = PollTrigger(
        name="Emails", 
        url="http://mycooldomain.com",
        template="An email has arrived...",
        interval=600
    )
    send_message_action = Action(
        id=390,
        function_name="send_message"
    )
    think_action = Action(
        id=391,
        function_name="think"
    )
    agent = Agent(
        id=75,
        name="Secretary",
        prompt="Manage the user's calendar and tasks",
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
        AssistantMessage('{"action": "think", "params": {"content": "I should notify the user of the new email"}}'),
        UserMessage("I should notify the user of the new email"),
        AssistantMessage('{"action": "send_message", "params": {"exchange_id": 3, "message": "A new email has arrived"}}'),
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
    mock_action_serv.get_tool_description.side_effect = lambda id: {
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
    
    
def test_monologue_service_throws_when_manipulating_nonexistent_monologue(db_serv, sample_monologue):
    # Arrange
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
