import pytest
from unittest import mock
from datetime import datetime, UTC
from sqlalchemy import select
from app.services.db import DatabaseService
from app.services.chat import ChatService, ChatSortMode, NonexistentChatError, NonexistentExchangeError, NonexistentMessageError, QueryAlreadyAnsweredError, CannotCreateChatForNonexistentUserError, ChatOptionsDiff
from app.model.user import User, Role
from app.model.chat import Chat
from app.model.chat_exchange import ChatExchange
from app.model.chat_message import ChatMessageMarkdown, ChatMessageChoicePrompt, ChatMessage, ChoiceMessageOption
from app.model.event import Event
from app.model.action import Action
from app.model.action_repository import ActionRepository
from app.model.trigger import ChatTrigger
from app.model.agent import Agent

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

def test_chat_service_can_get_all_chats_owned_by_user(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Horses",
                summary="Chat about horses",
                receiver="general",
                created_at=datetime.fromtimestamp(10, tz=UTC),
                modified_at=datetime.fromtimestamp(15, tz=UTC),
                exchanges=[
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(timestamp=datetime.fromtimestamp(14, tz=UTC))
                ]
            ),
            Chat(
                id=2,
                title="Goats",
                summary="Chat about goats",
                receiver="general",
                created_at=datetime.fromtimestamp(12, tz=UTC),
                modified_at=datetime.fromtimestamp(13, tz=UTC),
                exchanges=[
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC))
                ]
            )
        ]
    )
    user_victor = User(
        id=99,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Mules",
                summary="Chat about mules",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC)
            )
        ]
    )

    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()


    # Act
    res_recent = serv.get_user_chats(
        user_id=10,
        sort_by=ChatSortMode.RECENT
    )
    res_longest = serv.get_user_chats(
        user_id=10,
        sort_by=ChatSortMode.LONGEST
    )
    res_filtered = serv.get_user_chats(
        user_id=10,
        search_query="GoAT"
    )

    # Assert
    assert len(res_recent) == 2
    assert res_recent[0].id == 1
    assert res_recent[0].title == "Horses"
    assert res_recent[1].id == 2
    assert res_recent[1].title == "Goats"

    assert len(res_longest) == 2
    assert res_longest[0].id == 2
    assert res_longest[0].title == "Goats"
    assert res_longest[1].id == 1
    assert res_longest[1].title == "Horses"

    assert len(res_filtered) == 1
    assert res_filtered[0].id == 2
    assert res_filtered[0].title == "Goats"

def test_chat_service_returns_empty_list_when_getting_chats_for_nonexistent_user(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Horses",
                summary="Chat about horses",
                receiver="general",
                created_at=datetime.fromtimestamp(10, tz=UTC),
                modified_at=datetime.fromtimestamp(15, tz=UTC),
                exchanges=[
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(timestamp=datetime.fromtimestamp(14, tz=UTC))
                ]
            ),
            Chat(
                id=2,
                title="Goats",
                summary="Chat about goats",
                receiver="general",
                created_at=datetime.fromtimestamp(12, tz=UTC),
                modified_at=datetime.fromtimestamp(13, tz=UTC),
                exchanges=[
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC))
                ]
            )
        ]
    )
    user_victor = User(
        id=99,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Mules",
                summary="Chat about mules",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC)
            )
        ]
    )

    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    res = serv.get_user_chats(user_id=200)

    # Assert
    assert res == []


@mock.patch("app.services.chat.datetime")
def test_chat_service_can_create_new_blank_chat_for_user(mock_datetime, db_serv, db_session, trigger_mock):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(5000, tz=UTC)
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_victor = User(
        id=99,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Mules",
                summary="Chat about mules",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC)
            )
        ]
    )
    db_session.add(user_victor)
    db_session.commit()

    # Act
    created_id = serv.create_user_chat(user_id=99)

    # Assert
    chat = db_session.scalar(
        select(Chat).where(Chat.id == created_id)
    )
    assert len(user_victor.chats) == 2
    assert len(chat.exchanges) == 0
    assert chat.title == "Untitled"
    assert chat.summary == "No summary"
    assert chat.owner.id == 99
    assert chat.created_at.timestamp() == 5000
    assert chat.modified_at.timestamp() == 5000

def test_chat_service_throws_when_creating_new_chat_for_nonexistent_user(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_victor = User(
        id=99,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Mules",
                summary="Chat about mules",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC)
            )
        ]
    )
    db_session.add(user_victor)
    db_session.commit()

    # Act / Assert
    with pytest.raises(CannotCreateChatForNonexistentUserError):
        serv.create_user_chat(user_id=33333)

def test_chat_service_can_get_chat_by_id_including_allowed_actions(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    think_action = Action(
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action, think_action]
    )
    user = User(
        id=42,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                allowed_actions=[end_action, think_action]
            )
        ]
    )
    db_session.add(repo)
    db_session.add(user)
    db_session.commit()

    # Act
    res = serv.get_user_chat(42, 3)

    # Assert
    assert res.title == "Potatoes"
    assert res.summary == "KARTOFFELSALAD"
    assert len(res.allowed_actions) == 2
    assert res.allowed_actions[0].function_name == "end_workflow"
    assert res.allowed_actions[1].function_name == "think"

def test_chat_service_can_get_chat_receivers_of_user(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=10,
        username="John",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[
            ChatTrigger(
                name="General",
                template="",
                receiver="general"
            )
        ]
    )
    user_victor = User(
        id=42,
        username="Victor",
        password_hash="",
        role=Role.USER,
        allowed_triggers=[
            ChatTrigger(
                name="Research",
                template="",
                receiver="research"
            ),
            ChatTrigger(
                name="Technical",
                template="",
                receiver="technical"
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    res = serv.get_user_chat_receivers(42)
    res_nonexistent = serv.get_user_chat_receivers(100000)


    # Assert
    assert res == ["research", "technical"]
    assert res_nonexistent == []

def test_chat_service_can_remove_user_chat_including_exchanges_and_messages(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=2,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=3,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=4,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    user_victor = User(
        id=10,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Cars",
                summary="",
                receiver="technical",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                exchanges=[]
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    serv.remove_user_chat(user_id=5, chat_id=1)

    # Assert
    first_exchange = db_session.scalar(select(ChatExchange))
    first_message = db_session.scalar(select(ChatMessage))

    assert first_exchange is None
    assert first_message is None
    assert len(user_john.chats) == 1
    assert user_john.chats[0].title == "Potatoes"
    assert len(user_victor.chats) == 1
    assert user_victor.chats[0].title == "Cars"


def test_chat_service_can_duplicate_entire_user_chat(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=10,
                title="Carrots",
                summary="Sommery",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=10,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=10,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=20,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=20,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=30,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=40,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=20,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    user_victor = User(
        id=10,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=30,
                title="Cars",
                summary="",
                receiver="technical",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                exchanges=[]
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    duplicate_id = serv.duplicate_user_chat(user_id=5, chat_id=10)

    # Assert
    new_chat = db_session.scalar(
        select(Chat).where(Chat.id == duplicate_id)
    )

    assert len(user_john.chats) == 3
    assert new_chat is not None
    assert new_chat.id not in [10, 20, 30]
    assert new_chat.id == duplicate_id
    assert new_chat.title == "Carrots"
    assert new_chat.summary == "Sommery"
    assert new_chat.receiver == "general"
    assert new_chat.created_at == datetime.fromtimestamp(4000, tz=UTC)
    assert new_chat.modified_at == datetime.fromtimestamp(4350, tz=UTC)
    assert len(new_chat.exchanges) == 2
    assert new_chat.exchanges[0].id not in [10, 20]
    assert new_chat.exchanges[0].chat_id == duplicate_id
    assert new_chat.exchanges[0].timestamp == datetime.fromtimestamp(4200, tz=UTC)
    assert new_chat.exchanges[0].user_message.id not in [10, 20, 30, 40]
    assert new_chat.exchanges[0].user_message.markdown == "Hello!"
    assert new_chat.exchanges[0].agent_replies[0].id not in [10, 20, 30, 40]
    assert new_chat.exchanges[0].agent_replies[0].markdown == "What needs to be done?"
    assert new_chat.exchanges[1].id not in [10, 20]
    assert new_chat.exchanges[1].chat_id == duplicate_id
    assert new_chat.exchanges[1].timestamp == datetime.fromtimestamp(4300, tz=UTC)
    assert new_chat.exchanges[1].user_message.id not in [10, 20, 30, 40]
    assert new_chat.exchanges[1].user_message.markdown == "Find a book."
    assert new_chat.exchanges[1].agent_replies[0].id not in [10, 20, 30, 40]
    assert new_chat.exchanges[1].agent_replies[0].markdown == "Book found."


def test_chat_service_can_duplicate_user_chat_up_to_certain_exchange(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=10,
                title="Carrots",
                summary="Sommery",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=10,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=10,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=20,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=20,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=30,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=40,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    user_victor = User(
        id=10,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=30,
                title="Cars",
                summary="",
                receiver="technical",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                exchanges=[]
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act
    duplicate_id = serv.duplicate_user_chat(user_id=5, chat_id=10, last_exchange_id=10)

    # Assert
    new_chat = db_session.scalar(
        select(Chat).where(Chat.id == duplicate_id)
    )

    assert new_chat is not None
    assert new_chat.id not in [10, 20, 30]
    assert new_chat.id == duplicate_id
    assert new_chat.title == "Carrots"
    assert new_chat.summary == "Sommery"
    assert new_chat.receiver == "general"
    assert new_chat.created_at == datetime.fromtimestamp(4000, tz=UTC)
    assert new_chat.modified_at == datetime.fromtimestamp(4350, tz=UTC)
    assert len(new_chat.exchanges) == 1
    assert new_chat.exchanges[0].id not in [10, 20]
    assert new_chat.exchanges[0].timestamp == datetime.fromtimestamp(4200, tz=UTC)
    assert new_chat.exchanges[0].user_message.id not in [10, 20, 30, 40]
    assert new_chat.exchanges[0].user_message.markdown == "Hello!"
    assert new_chat.exchanges[0].agent_replies[0].id not in [10, 20, 30, 40]
    assert new_chat.exchanges[0].agent_replies[0].markdown == "What needs to be done?"

def test_chat_service_throws_when_invalid_last_exchange_id_specified_during_duplicate(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="Sommery",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=2,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=3,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=4,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    user_victor = User(
        id=10,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Cars",
                summary="",
                receiver="technical",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=3,
                        timestamp=datetime.fromtimestamp(2000, tz=UTC)
                    )
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentExchangeError):
        serv.duplicate_user_chat(user_id=5, chat_id=1, last_exchange_id=3)



@mock.patch("app.services.chat.datetime")
def test_chat_service_can_send_markdown_message_to_user_chat_from_user(mock_datetime, db_serv, db_session, trigger_mock):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(15000, tz=UTC)
    def receive_chat_message_mock(receiver: str, message: str):
        event1 = Event(
            id=1,
            content="A message has arrived: That's not it",
            dispatched=True
        )
        event2 = Event(
            id=2,
            content="MSG: That's not it",
            dispatched=True
        )
        db_session.add(event1)
        db_session.add(event2)
        db_session.commit()
        return [1, 2]

    trigger_mock.receive_chat_message.side_effect = receive_chat_message_mock
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=10,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=10,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=20,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=20,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=30,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=40,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.commit()

    # Act
    exchange_id = serv.send_markdown_message_to_user_chat(
        user_id=5,
        chat_id=1,
        from_agent_id=None,
        markdown="That's not it"
    )

    # Assert
    # ...user messages sent to a chat can set off ChatTriggers
    trigger_mock.receive_chat_message.assert_called_with(
        receiver="general",
        message="That's not it"
    )

    db_session.refresh(user_john)
    assert len(user_john.chats[0].exchanges) == 3
    assert user_john.chats[0].modified_at == datetime.fromtimestamp(15000, tz=UTC)
    assert user_john.chats[0].exchanges[2].id == exchange_id

    exchange = db_session.scalar(
        select(ChatExchange).where(ChatExchange.id == exchange_id)
    )
    assert exchange.timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert exchange.user_message.timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert exchange.user_message.markdown == "That's not it"
    assert exchange.user_message.sending_user.id == 5
    assert exchange.user_message.sending_user.username == "John"
    assert len(exchange.agent_replies) == 0


@mock.patch("app.services.chat.datetime")
def test_chat_service_can_send_markdown_message_to_user_chat_from_agent(mock_datetime, db_serv, db_session, trigger_mock):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(15000, tz=UTC)
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=10,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=10,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=20,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=20,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=30,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=40,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    agent = Agent(
        id=12,
        name="Librarian",
        prompt="You are a librarian",
        owner=user_john
    )
    db_session.add(user_john)
    db_session.add(agent)
    db_session.commit()

    # Act
    exchange_id = serv.send_markdown_message_to_user_chat(
        user_id=5,
        chat_id=1,
        from_agent_id=12,
        markdown="Oops"
    )

    # Assert
    # ...agent messages sent to a chat CANNOT set off ChatTriggers
    trigger_mock.receive_chat_message.assert_not_called()

    db_session.refresh(user_john)
    assert len(user_john.chats[0].exchanges) == 3
    assert user_john.chats[0].modified_at == datetime.fromtimestamp(15000, tz=UTC)
    assert user_john.chats[0].exchanges[2].id == exchange_id

    exchange = db_session.scalar(
        select(ChatExchange).where(ChatExchange.id == exchange_id)
    )
    assert exchange.timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert exchange.user_message is None
    assert len(exchange.agent_replies) == 1
    assert exchange.agent_replies[0].timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert exchange.agent_replies[0].markdown == "Oops"
    assert exchange.agent_replies[0].sending_agent.id == 12
    assert exchange.agent_replies[0].sending_agent.name == "Librarian"

@mock.patch("app.services.chat.datetime")
def test_chat_service_can_send_choice_message_to_user_chat_from_agent(mock_datetime, db_serv, db_session, trigger_mock):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(15000, tz=UTC)
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=10,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=10,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=20,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=20,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=30,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=40,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    agent = Agent(
        id=12,
        name="Librarian",
        prompt="You are a librarian",
        owner=user_john
    )
    db_session.add(user_john)
    db_session.add(agent)
    db_session.commit()

    # Act
    exchange_id, query_id = serv.send_choice_message_to_user_chat(
        user_id=5,
        chat_id=1,
        from_agent_id=12,
        prompt="What should I do?",
        choices=[20, "no"]
    )

    # Assert
    # ...agent messages sent to a chat CANNOT set off ChatTriggers
    trigger_mock.receive_chat_message.assert_not_called()

    db_session.refresh(user_john)
    assert len(user_john.chats[0].exchanges) == 3
    assert user_john.chats[0].modified_at == datetime.fromtimestamp(15000, tz=UTC)
    assert user_john.chats[0].exchanges[2].id == exchange_id

    exchange = db_session.scalar(
        select(ChatExchange).where(ChatExchange.id == exchange_id)
    )
    assert exchange.timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert exchange.user_message is None
    assert len(exchange.agent_replies) == 1
    assert exchange.agent_replies[0].id == query_id

    message = db_session.scalar(
        select(ChatMessageChoicePrompt).where(ChatMessageChoicePrompt.id == query_id)
    )
    assert message.timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert message.prompt == "What should I do?"
    assert len(message.choices) == 2
    assert message.choices[0].value == 20
    assert message.choices[1].value == "no"

@mock.patch("app.services.chat.datetime")
def test_chat_service_can_send_markdown_reply_to_user_exchange_from_agent(mock_datetime, db_serv, db_session, trigger_mock):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(15000, tz=UTC)
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=20,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    agent = Agent(
        id=12,
        name="Librarian",
        prompt="You are a librarian",
        owner=user_john
    )
    db_session.add(user_john)
    db_session.add(agent)
    db_session.commit()

    # Act
    serv.send_markdown_reply_to_user_exchange(
        user_id=5,
        exchange_id=1,
        from_agent_id=12,
        markdown="What can I do for you?"
    )

    # Assert
    # ...agent replies CANNOT set off ChatTriggers
    trigger_mock.receive_chat_message.assert_not_called()

    db_session.refresh(user_john)
    assert len(user_john.chats[0].exchanges) == 1
    assert user_john.chats[0].modified_at == datetime.fromtimestamp(15000, tz=UTC)

    exchange = user_john.chats[0].exchanges[0]
    assert exchange.timestamp == datetime.fromtimestamp(4200, tz=UTC)
    assert len(exchange.agent_replies) == 1
    assert exchange.agent_replies[0].timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert exchange.agent_replies[0].markdown == "What can I do for you?"
    assert exchange.agent_replies[0].sending_agent.id == 12
    assert exchange.agent_replies[0].sending_agent.name == "Librarian"

@mock.patch("app.services.chat.datetime")
def test_chat_service_can_send_choice_reply_to_user_exchange_from_agent(mock_datetime, db_serv, db_session, trigger_mock):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(15000, tz=UTC)
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=10,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    agent = Agent(
        id=12,
        name="Librarian",
        prompt="You are a librarian",
        owner=user_john
    )
    db_session.add(user_john)
    db_session.add(agent)
    db_session.commit()

    # Act
    query_id = serv.send_choice_reply_to_user_exchange(
        user_id=5,
        exchange_id=1,
        from_agent_id=12,
        prompt="What should I do?",
        choices=[20, "no"]
    )

    # Assert
    # ...agent replies CANNOT set off ChatTriggers
    trigger_mock.receive_chat_message.assert_not_called()

    db_session.refresh(user_john)
    assert len(user_john.chats[0].exchanges) == 1
    assert user_john.chats[0].modified_at == datetime.fromtimestamp(15000, tz=UTC)

    exchange = user_john.chats[0].exchanges[0]
    assert exchange.timestamp == datetime.fromtimestamp(4200, tz=UTC)
    assert len(exchange.agent_replies) == 1
    assert exchange.agent_replies[0].id == query_id

    message = exchange.agent_replies[0]
    assert message.timestamp == datetime.fromtimestamp(15000, tz=UTC)
    assert message.prompt == "What should I do?"
    assert len(message.choices) == 2
    assert message.choices[0].value == 20
    assert message.choices[1].value == "no"

@mock.patch("app.services.chat.datetime")
def test_chat_service_leaves_agent_field_blank_for_sent_messages_for_nonexistent_agent_ids(mock_datetime, db_serv, db_session, trigger_mock):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(15000, tz=UTC)
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=10,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=10,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    agent = Agent(
        id=12,
        name="Librarian",
        prompt="You are a librarian",
        owner=user_john
    )
    db_session.add(user_john)
    db_session.add(agent)
    db_session.commit()

    # Act
    exchange_id_md = serv.send_markdown_message_to_user_chat(
        user_id=5,
        chat_id=2,
        from_agent_id=9999,
        markdown="Hello"
    )
    exchange_id_choice = serv.send_choice_message_to_user_chat(
        user_id=5,
        chat_id=2,
        from_agent_id=9999,
        prompt="What should be done?",
        choices=["There is nothing we can do"]
    )
    serv.send_markdown_reply_to_user_exchange(
        user_id=5,
        exchange_id=10,
        from_agent_id=9999,
        markdown="Hello, what can I do for you?"
    )
    serv.send_choice_reply_to_user_exchange(
        user_id=5,
        exchange_id=10,
        from_agent_id=9999,
        prompt="What should I do?",
        choices=[20, "no"]
    )

    # Assert
    exchange_md = db_session.scalar(
        select(ChatExchange).where(ChatExchange.id == exchange_id_md)
    )
    assert exchange_md.agent_replies[0].sending_user is None
    assert exchange_md.agent_replies[0].sending_agent is None
    exchange_choice = db_session.scalar(
        select(ChatExchange).where(ChatExchange.id == exchange_id_choice[0])
    )
    assert exchange_choice.agent_replies[0].sending_user is None
    assert exchange_choice.agent_replies[0].sending_agent is None
    reply_exchange = db_session.scalar(
        select(ChatExchange).where(ChatExchange.id == 10)
    )
    assert reply_exchange.agent_replies[0].sending_user is None
    assert reply_exchange.agent_replies[0].sending_agent is None
    assert reply_exchange.agent_replies[1].sending_user is None
    assert reply_exchange.agent_replies[1].sending_agent is None


def test_chat_service_can_get_exchanges_after_timestamp_including_user_message(db_serv, db_session, trigger_mock):
    # Arrange
    # TODO: Test how the user message behaves when its a ChatMessageChoicePrompt?
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(4200, tz=UTC),
                                markdown="What needs to be done?"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=2,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=3,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=4,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    ),
                    ChatExchange(
                        id=3,
                        timestamp=datetime.fromtimestamp(5000, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=5,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Really?"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=6,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Really."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    agent = Agent(
        id=12,
        name="Librarian",
        prompt="You are a librarian",
        owner=user_john
    )
    db_session.add(user_john)
    db_session.add(agent)
    db_session.commit()

    # Act
    res3 = serv.get_user_chat_exchanges_after(
        user_id=5,
        chat_id=1,
        after=0
    )
    res2 = serv.get_user_chat_exchanges_after(
        user_id=5,
        chat_id=1,
        after=4200
    )
    res1 = serv.get_user_chat_exchanges_after(
        user_id=5,
        chat_id=1,
        after=4300
    )

    # Assert
    assert len(res3) == 3
    assert res3[0].id == 1
    assert isinstance(res3[0].user_message, ChatMessageMarkdown)
    assert res3[0].user_message.markdown == "Hello!"
    assert res3[1].id == 2
    assert isinstance(res3[1].user_message, ChatMessageMarkdown)
    assert res3[1].user_message.markdown == "Find a book."
    assert res3[2].id == 3
    assert isinstance(res3[2].user_message, ChatMessageMarkdown)
    assert res3[2].user_message.markdown == "Really?"

    assert len(res2) == 2
    assert res2[0].id == 2
    assert isinstance(res2[0].user_message, ChatMessageMarkdown)
    assert res2[0].user_message.markdown == "Find a book."
    assert res2[1].id == 3
    assert isinstance(res2[1].user_message, ChatMessageMarkdown)
    assert res2[1].user_message.markdown == "Really?"

    assert len(res1) == 1
    assert res1[0].id == 3
    assert isinstance(res1[0].user_message, ChatMessageMarkdown)
    assert res1[0].user_message.markdown == "Really?"


def test_chat_service_can_get_exchange_replies_after_timestamp(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(5000, tz=UTC),
                                markdown="First reply"
                            ),
                            ChatMessageMarkdown(
                                id=3,
                                timestamp=datetime.fromtimestamp(6000, tz=UTC),
                                markdown="Second reply"
                            ),
                            ChatMessageChoicePrompt(
                                id=4,
                                timestamp=datetime.fromtimestamp(7000, tz=UTC),
                                prompt="Third reply",
                                choices=[
                                    ChoiceMessageOption(value=10),
                                    ChoiceMessageOption(value="lol")
                                ]
                            )
                        ]
                    ),
                    ChatExchange(
                        id=2,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=5,
                            timestamp=datetime.fromtimestamp(4300, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=6,
                                timestamp=datetime.fromtimestamp(4350, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    agent = Agent(
        id=12,
        name="Librarian",
        prompt="You are a librarian",
        owner=user_john
    )
    db_session.add(user_john)
    db_session.add(agent)
    db_session.commit()

    # Act
    res3 = serv.get_user_exchange_replies_after(
        user_id=5,
        exchange_id=1,
        after=0
    )
    res2 = serv.get_user_exchange_replies_after(
        user_id=5,
        exchange_id=1,
        after=5000
    )
    res1 = serv.get_user_exchange_replies_after(
        user_id=5,
        exchange_id=1,
        after=6000
    )
    res0 = serv.get_user_exchange_replies_after(
        user_id=5,
        exchange_id=1,
        after=7000
    )

    assert len(res3) == 3
    assert isinstance(res3[0], ChatMessageMarkdown)
    assert res3[0].markdown == "First reply"
    assert isinstance(res3[1], ChatMessageMarkdown)
    assert res3[1].markdown == "Second reply"
    assert isinstance(res3[2], ChatMessageChoicePrompt)
    assert res3[2].prompt == "Third reply"
    assert len(res3[2].choices) == 2
    assert res3[2].choices[0].value == 10
    assert res3[2].choices[1].value == "lol"

    assert len(res2) == 2
    assert isinstance(res2[0], ChatMessageMarkdown)
    assert res2[0].markdown == "Second reply"
    assert isinstance(res2[1], ChatMessageChoicePrompt)
    assert res2[1].prompt == "Third reply"
    assert len(res2[1].choices) == 2
    assert res2[1].choices[0].value == 10
    assert res2[1].choices[1].value == "lol"

    assert len(res1) == 1
    assert isinstance(res1[0], ChatMessageChoicePrompt)
    assert res1[0].prompt == "Third reply"
    assert len(res1[0].choices) == 2
    assert res1[0].choices[0].value == 10
    assert res1[0].choices[1].value == "lol"

    assert len(res0) == 0

def test_chat_service_can_set_chat_options(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    think_action = Action(
        id=1,
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        id=2,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action, think_action]
    )
    user = User(
        id=42,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                allowed_actions=[end_action, think_action]
            )
        ],
        allowed_actions=[end_action, think_action]
    )
    db_session.add(repo)
    db_session.add(user)
    db_session.commit()

    # Act
    serv.update_user_chat_options(
        user_id=42,
        chat_id=3,
        options=ChatOptionsDiff(
            receiver="technical"
        )
    )

    # Assert
    db_session.refresh(user)
    assert user.chats[0].receiver == "technical"
    assert len(user.chats[0].allowed_actions) == 2

    # Act
    serv.update_user_chat_options(
        user_id=42,
        chat_id=3,
        options=ChatOptionsDiff(
            receiver="new",
            enabled_action_ids=[1]
        )
    )

    # Assert
    db_session.refresh(user)
    assert user.chats[0].receiver == "new"
    assert len(user.chats[0].allowed_actions) == 1
    assert user.chats[0].allowed_actions[0].function_name == "think"


def test_chat_service_ignores_nonexistent_or_disallowed_action_ids_when_setting_chat_options(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    think_action = Action(
        id=1,
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        id=2,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    search_action = Action(
        id=3,
        function_name="search_web",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action, think_action, search_action]
    )
    user = User(
        id=42,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                allowed_actions=[end_action, think_action]
            )
        ],
        allowed_actions=[end_action, think_action]
    )
    db_session.add(repo)
    db_session.add(user)
    db_session.commit()

    # Act
    serv.update_user_chat_options(
        user_id=42,
        chat_id=3,
        options=ChatOptionsDiff(
            enabled_action_ids=[1, 3, 99]
        )
    )

    # Assert
    db_session.refresh(user)
    assert len(user.chats[0].allowed_actions) == 1
    assert user.chats[0].allowed_actions[0].function_name == "think"

def test_chat_service_can_set_user_chat_summary(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    think_action = Action(
        id=1,
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        id=2,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    search_action = Action(
        id=3,
        function_name="search_web",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action, think_action, search_action]
    )
    user = User(
        id=42,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=3,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                allowed_actions=[end_action, think_action]
            )
        ],
        allowed_actions=[end_action, think_action]
    )
    db_session.add(repo)
    db_session.add(user)
    db_session.commit()

    # Act
    serv.set_user_chat_summary(
        user_id=42,
        chat_id=3,
        summary="new"
    )

    # Assert
    db_session.refresh(user)
    assert user.chats[0].summary == "new"

def test_chat_service_can_get_all_messages_from_user_chat_flattened(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(5000, tz=UTC),
                                markdown="First reply"
                            ),
                            ChatMessageMarkdown(
                                id=3,
                                timestamp=datetime.fromtimestamp(6000, tz=UTC),
                                markdown="Second reply"
                            ),
                            ChatMessageMarkdown(
                                id=4,
                                timestamp=datetime.fromtimestamp(7000, tz=UTC),
                                markdown="Third reply"
                            )
                        ]
                    ),
                    ChatExchange(
                        id=2,
                        timestamp=datetime.fromtimestamp(4300, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=5,
                            timestamp=datetime.fromtimestamp(9000, tz=UTC),
                            markdown="Find a book."
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=6,
                                timestamp=datetime.fromtimestamp(10000, tz=UTC),
                                markdown="Book found."
                            )
                        ]
                    ),
                    ChatExchange(
                        id=3,
                        timestamp=datetime.fromtimestamp(11000, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=7,
                            timestamp=datetime.fromtimestamp(11000, tz=UTC),
                            markdown="That's not it!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=8,
                                timestamp=datetime.fromtimestamp(12000, tz=UTC),
                                markdown="Really?"
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.commit()

    # Act
    res = serv.get_user_chat_messages(
        user_id=5,
        chat_id=1
    )

    # Assert
    assert len(res) == 8
    assert isinstance(res[0], ChatMessageMarkdown)
    assert res[0].markdown == "Hello!"
    assert isinstance(res[1], ChatMessageMarkdown)
    assert res[1].markdown == "First reply"
    assert isinstance(res[2], ChatMessageMarkdown)
    assert res[2].markdown == "Second reply"
    assert isinstance(res[3], ChatMessageMarkdown)
    assert res[3].markdown == "Third reply"
    assert isinstance(res[4], ChatMessageMarkdown)
    assert res[4].markdown == "Find a book."
    assert isinstance(res[5], ChatMessageMarkdown)
    assert res[5].markdown == "Book found."
    assert isinstance(res[6], ChatMessageMarkdown)
    assert res[6].markdown == "That's not it!"
    assert isinstance(res[7], ChatMessageMarkdown)
    assert res[7].markdown == "Really?"

def test_chat_service_can_get_answered_query_answer_of_choice_message(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(5000, tz=UTC),
                                markdown="First reply"
                            ),
                            ChatMessageChoicePrompt(
                                id=10,
                                prompt="Answer?",
                                answer={ "woo": 20 },
                                timestamp=datetime.fromtimestamp(10000, tz=UTC)
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.commit()

    # Act
    res = serv.get_user_query_answer(
        user_id=5,
        message_id=10
    )

    # Assert
    assert res == { "woo": 20 }

def test_chat_service_returns_None_when_getting_answer_for_unanswered_query_of_choice_message(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(5000, tz=UTC),
                                markdown="First reply"
                            ),
                            ChatMessageChoicePrompt(
                                id=10,
                                prompt="Answer?",
                                timestamp=datetime.fromtimestamp(10000, tz=UTC)
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.commit()

    # Act
    res = serv.get_user_query_answer(
        user_id=5,
        message_id=10
    )

    # Assert
    assert res is None

def test_chat_service_can_set_unanswered_query_answer(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(5000, tz=UTC),
                                markdown="First reply"
                            ),
                            ChatMessageChoicePrompt(
                                id=10,
                                prompt="Answer?",
                                timestamp=datetime.fromtimestamp(10000, tz=UTC)
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.commit()

    # Act
    serv.set_user_query_answer(
        user_id=5,
        message_id=10,
        answer=[200, "wee"]
    )

    # Assert
    choice = db_session.scalar(
        select(ChatMessageChoicePrompt).where(ChatMessageChoicePrompt.id == 10)
    )
    assert choice.answer == [200, "wee"]

def test_chat_service_throws_when_setting_answer_for_answered_query(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_john = User(
        id=5,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Carrots",
                summary="",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4350, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(4200, tz=UTC),
                        user_message=ChatMessageMarkdown(
                            id=1,
                            timestamp=datetime.fromtimestamp(4200, tz=UTC),
                            markdown="Hello!"
                        ),
                        agent_replies=[
                            ChatMessageMarkdown(
                                id=2,
                                timestamp=datetime.fromtimestamp(5000, tz=UTC),
                                markdown="First reply"
                            ),
                            ChatMessageChoicePrompt(
                                id=10,
                                prompt="Answer?",
                                answer=True,
                                timestamp=datetime.fromtimestamp(10000, tz=UTC)
                            )
                        ]
                    )
                ]
            ),
            Chat(
                id=2,
                title="Potatoes",
                summary="KARTOFFELSALAD",
                receiver="general",
                created_at=datetime.fromtimestamp(7000, tz=UTC),
                modified_at=datetime.fromtimestamp(12000, tz=UTC),
                exchanges=[
                ]
            )
        ]
    )
    db_session.add(user_john)
    db_session.commit()

    # Act / Assert
    with pytest.raises(QueryAlreadyAnsweredError):
        serv.set_user_query_answer(
            user_id=5,
            message_id=10,
            answer=[200, "wee"]
        )


def test_chat_service_throws_when_trying_to_manipulate_nonexistent_chat(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_victor = User(
        id=1,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Mules",
                summary="Chat about mules",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC)
            )
        ]
    )
    user_john = User(
        id=2,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=2,
                title="Horses",
                summary="Chat about horses",
                receiver="general",
                created_at=datetime.fromtimestamp(10, tz=UTC),
                modified_at=datetime.fromtimestamp(15, tz=UTC),
                exchanges=[
                    ChatExchange(timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(timestamp=datetime.fromtimestamp(14, tz=UTC))
                ]
            )
        ]
    )


    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentChatError):
        serv.get_user_chat(
            user_id=1,
            chat_id=3 # Nonexistent
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat(
            user_id=1,
            chat_id=2 # Not owned by ID 1
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat(
            user_id=3, # Nonexistent
            chat_id=2
        )

    with pytest.raises(NonexistentChatError):
        serv.remove_user_chat(
            user_id=1,
            chat_id=3 # Nonexistent
        )

    with pytest.raises(NonexistentChatError):
        serv.remove_user_chat(
            user_id=1,
            chat_id=2 # Not owned by ID 1
        )

    with pytest.raises(NonexistentChatError):
        serv.remove_user_chat(
            user_id=3, # Nonexistent
            chat_id=2
        )

    with pytest.raises(NonexistentChatError):
        serv.duplicate_user_chat(
            user_id=1,
            chat_id=3 # Nonexistent
        )

    with pytest.raises(NonexistentChatError):
        serv.duplicate_user_chat(
            user_id=1,
            chat_id=2 # Not owned by ID 1
        )

    with pytest.raises(NonexistentChatError):
        serv.duplicate_user_chat(
            user_id=3, # Nonexistent
            chat_id=2
        )

    with pytest.raises(NonexistentChatError):
        serv.send_markdown_message_to_user_chat(
            user_id=1,
            chat_id=3, # Nonexistent
            from_agent_id=None,
            markdown=""
        )

    with pytest.raises(NonexistentChatError):
        serv.send_markdown_message_to_user_chat(
            user_id=1,
            chat_id=2, # Not owned by ID 1
            from_agent_id=None,
            markdown=""
        )

    with pytest.raises(NonexistentChatError):
        serv.send_markdown_message_to_user_chat(
            user_id=3, # Nonexistent
            chat_id=2,
            from_agent_id=None,
            markdown=""
        )

    with pytest.raises(NonexistentChatError):
        serv.send_choice_message_to_user_chat(
            user_id=1,
            chat_id=3, # Nonexistent
            from_agent_id=None,
            prompt="",
            choices=[]
        )

    with pytest.raises(NonexistentChatError):
        serv.send_choice_message_to_user_chat(
            user_id=1,
            chat_id=2, # Not owned by ID 1
            from_agent_id=None,
            prompt="",
            choices=[]
        )

    with pytest.raises(NonexistentChatError):
        serv.send_choice_message_to_user_chat(
            user_id=3, # Nonexistent
            chat_id=2,
            from_agent_id=None,
            prompt="",
            choices=[]
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat_exchanges_after(
            user_id=1,
            chat_id=3, # Nonexistent
            after=0
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat_exchanges_after(
            user_id=1,
            chat_id=2, # Not owned by ID 1
            after=0
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat_exchanges_after(
            user_id=3, # Nonexistent
            chat_id=2,
            after=0
        )

    with pytest.raises(NonexistentChatError):
        serv.update_user_chat_options(
            user_id=1,
            chat_id=3, # Nonexistent
            options=ChatOptionsDiff()
        )

    with pytest.raises(NonexistentChatError):
        serv.update_user_chat_options(
            user_id=1,
            chat_id=2, # Not owned by ID 1
            options=ChatOptionsDiff()
        )

    with pytest.raises(NonexistentChatError):
        serv.update_user_chat_options(
            user_id=3, # Nonexistent
            chat_id=2,
            options=ChatOptionsDiff()
        )

    with pytest.raises(NonexistentChatError):
        serv.set_user_chat_summary(
            user_id=1,
            chat_id=3, # Nonexistent
            summary=""
        )

    with pytest.raises(NonexistentChatError):
        serv.set_user_chat_summary(
            user_id=1,
            chat_id=2, # Not owned by ID 1
            summary=""
        )

    with pytest.raises(NonexistentChatError):
        serv.set_user_chat_summary(
            user_id=3, # Nonexistent
            chat_id=2,
            summary=""
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat_messages(
            user_id=1,
            chat_id=3, # Nonexistent
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat_messages(
            user_id=1,
            chat_id=2, # Not owned by ID 1
        )

    with pytest.raises(NonexistentChatError):
        serv.get_user_chat_messages(
            user_id=3, # Nonexistent
            chat_id=2,
        )


def test_chat_service_throws_when_trying_to_manipulate_nonexistent_exchange(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_victor = User(
        id=1,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Mules",
                summary="Chat about mules",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                exchanges=[
                    ChatExchange(id=1, timestamp=datetime.fromtimestamp(5, tz=UTC))
                ]
            )
        ]
    )
    user_john = User(
        id=2,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=2,
                title="Horses",
                summary="Chat about horses",
                receiver="general",
                created_at=datetime.fromtimestamp(10, tz=UTC),
                modified_at=datetime.fromtimestamp(15, tz=UTC),
                exchanges=[
                    ChatExchange(id=2, timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(id=3, timestamp=datetime.fromtimestamp(14, tz=UTC))
                ]
            )
        ]
    )


    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentExchangeError):
        serv.send_markdown_reply_to_user_exchange(
            user_id=1,
            exchange_id=100, # Nonexistent
            from_agent_id=None,
            markdown=""
        )

    with pytest.raises(NonexistentExchangeError):
        serv.send_markdown_reply_to_user_exchange(
            user_id=1,
            exchange_id=2, # Not owned by ID 1
            from_agent_id=None,
            markdown=""
        )

    with pytest.raises(NonexistentExchangeError):
        serv.send_markdown_reply_to_user_exchange(
            user_id=3, # Nonexistent
            exchange_id=2, 
            from_agent_id=None,
            markdown=""
        )

    with pytest.raises(NonexistentExchangeError):
        serv.send_choice_reply_to_user_exchange(
            user_id=1,
            exchange_id=100, # Nonexistent
            from_agent_id=None,
            prompt="",
            choices=[]
        )

    with pytest.raises(NonexistentExchangeError):
        serv.send_choice_reply_to_user_exchange(
            user_id=1,
            exchange_id=2, # Not owned by ID 1
            from_agent_id=None,
            prompt="",
            choices=[]
        )

    with pytest.raises(NonexistentExchangeError):
        serv.send_choice_reply_to_user_exchange(
            user_id=3, # Nonexistent
            exchange_id=2, 
            from_agent_id=None,
            prompt="",
            choices=[]
        )

    with pytest.raises(NonexistentExchangeError):
        serv.get_user_exchange_replies_after(
            user_id=1,
            exchange_id=100, # Nonexistent
            after=0
        )

    with pytest.raises(NonexistentExchangeError):
        serv.get_user_exchange_replies_after(
            user_id=1,
            exchange_id=2, # Not owned by ID 1
            after=0
        )

    with pytest.raises(NonexistentExchangeError):
        serv.get_user_exchange_replies_after(
            user_id=3, # Nonexistent
            exchange_id=2, 
            after=0
        )

def test_chat_service_throws_when_trying_to_manipulate_nonexistent_message(db_serv, db_session, trigger_mock):
    # Arrange
    serv = ChatService(
        database_service=db_serv,
        trigger_service=trigger_mock
    )
    user_victor = User(
        id=1,
        username="Victor",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=1,
                title="Mules",
                summary="Chat about mules",
                receiver="general",
                created_at=datetime.fromtimestamp(4000, tz=UTC),
                modified_at=datetime.fromtimestamp(4200, tz=UTC),
                exchanges=[
                    ChatExchange(
                        id=1,
                        timestamp=datetime.fromtimestamp(5, tz=UTC),
                        agent_replies=[
                            ChatMessageChoicePrompt(
                                id=1,
                                prompt="Answer?",
                                answer={ "woo": 20 },
                                timestamp=datetime.fromtimestamp(10000, tz=UTC)
                            )
                        ]
                    )
                ]
            )
        ]
    )
    user_john = User(
        id=2,
        username="John",
        password_hash="",
        role=Role.USER,
        chats=[
            Chat(
                id=2,
                title="Horses",
                summary="Chat about horses",
                receiver="general",
                created_at=datetime.fromtimestamp(10, tz=UTC),
                modified_at=datetime.fromtimestamp(15, tz=UTC),
                exchanges=[
                    ChatExchange(id=2, timestamp=datetime.fromtimestamp(12, tz=UTC)),
                    ChatExchange(
                        id=3,
                        timestamp=datetime.fromtimestamp(14, tz=UTC),
                        agent_replies=[
                            ChatMessageChoicePrompt(
                                id=2,
                                prompt="Answer?",
                                answer={ "woo": 20 },
                                timestamp=datetime.fromtimestamp(10000, tz=UTC)
                            )
                        ]
                    )
                ]
            )
        ]
    )

    db_session.add(user_john)
    db_session.add(user_victor)
    db_session.commit()

    # Act / Assert
    with pytest.raises(NonexistentMessageError):
        serv.get_user_query_answer(
            user_id=1,
            message_id=999, # Nonexistent
        )

    with pytest.raises(NonexistentMessageError):
        serv.get_user_query_answer(
            user_id=1,
            message_id=2, # Not owned by ID 1
        )

    with pytest.raises(NonexistentMessageError):
        serv.get_user_query_answer(
            user_id=9000, # Nonexistent
            message_id=2 
        )

    with pytest.raises(NonexistentMessageError):
        serv.set_user_query_answer(
            user_id=1,
            message_id=999, # Nonexistent
            answer=""
        )

    with pytest.raises(NonexistentMessageError):
        serv.set_user_query_answer(
            user_id=1,
            message_id=2, # Not owned by ID 1
            answer=""
        )

    with pytest.raises(NonexistentMessageError):
        serv.set_user_query_answer(
            user_id=9000, # Nonexistent
            message_id=2,
            answer=""
        )
