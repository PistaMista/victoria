from pydantic import BaseModel
from typing import Optional, List, Any, Tuple
from enum import Enum
from sqlalchemy import select, func, distinct, or_
from sqlalchemy.orm import Session, joinedload, undefer, with_polymorphic
from app.services.db import DatabaseService
from app.services.trigger import TriggerService
from app.services import event_bus
from app.model.trigger import ChatTrigger
from app.model.action import Action
from app.model.user import User
from app.model.agent import Agent
from app.model.chat import Chat
from app.model.event import Event
from app.model.chat_exchange import ChatExchange
from app.model.chat_message import (
    ChatMessage,
    ChatMessageMarkdown,
    ChatMessageChoicePrompt,
    ChoiceMessageOption,
)
from datetime import datetime, UTC
from dataclasses import dataclass


class ChatSortMode(Enum):
    LONGEST = 0
    RECENT = 1


class ChatService:
    def __init__(
        self,
        database_service: DatabaseService,
        trigger_service: TriggerService,
        event_bus_service: event_bus.EventBusService,
    ):
        self._db: DatabaseService = database_service
        self._trigger: TriggerService = trigger_service
        self._event_bus: event_bus.EventBusService = event_bus_service

    def get_user_chats(
        self,
        user_id: int,
        sort_by: ChatSortMode = ChatSortMode.RECENT,
        search_query: Optional[str] = None,
    ) -> List[Chat]:
        """Gets all chats of the given User."""
        with self._db.session() as db:
            stmt = select(Chat).where(Chat.owner_id == user_id)

            if search_query is not None:
                stmt = stmt.where(
                    or_(
                        func.lower(Chat.title).like(f"%{search_query.lower()}%"),
                        func.lower(Chat.summary).like(f"%{search_query.lower()}%"),
                    )
                )

            match sort_by:
                case ChatSortMode.RECENT:
                    stmt = stmt.order_by(Chat.modified_at.desc())
                case ChatSortMode.LONGEST:
                    stmt = (
                        stmt.outerjoin(Chat.exchanges)
                        .group_by(Chat.id)
                        .order_by(func.count(ChatExchange.id).desc())
                    )

            res = db.scalars(stmt).all()
            return res

    def create_user_chat(self, user_id: int) -> int:
        """Creates a new blank chat for a user and returns its id."""
        with self._db.session() as db:
            user = db.scalar(select(User).where(User.id == user_id))

            if user is None:
                raise CannotCreateChatForNonexistentUserError(user_id)

            new_chat = Chat(
                title="Untitled",
                summary="No summary",
                receiver="",
                created_at=datetime.now(tz=UTC),
                modified_at=datetime.now(tz=UTC),
                owner=user,
            )

            db.add(new_chat)
            db.commit()

            self._event_bus.publish(
                ChatCreatedEvent(user_id=new_chat.owner_id, chat_id=new_chat.id)
            )
            return new_chat.id

    def get_user_chat(self, user_id: int, chat_id: int) -> Chat:
        """Gets a User's chat."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)

            db.refresh(chat, ["allowed_actions"])
            return chat

    def get_user_chat_receivers(self, user_id: int) -> List[str]:
        """Gets all the valid chat receivers for the given User."""
        with self._db.session() as db:
            stmt = (
                select(distinct(ChatTrigger.receiver))
                .join(User.allowed_triggers.of_type(ChatTrigger))
                .where(User.id == user_id)
            )
            res = db.scalars(stmt).all()

            return res

    def remove_user_chat(self, user_id: int, chat_id: int):
        """Deletes the given Chat."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)
            db.delete(chat)
            db.commit()

            self._event_bus.publish(ChatDeletedEvent(user_id=user_id, chat_id=chat_id))

    def duplicate_user_chat(
        self, user_id: int, chat_id: int, last_exchange_id: Optional[int] = None
    ) -> int:
        """Duplicates the given Chat up to the given Exchange and returns the new id."""
        with self._db.session() as db:
            old_chat = self._load_user_chat(db, user_id, chat_id)
            new_chat = self._clone_scalar_fields(old_chat)

            required_last_exchange_found = last_exchange_id is None
            for old_exchange in old_chat.exchanges:
                new_exchange = self._clone_scalar_fields(old_exchange)

                if old_exchange.user_message is not None:
                    new_user_message = self._clone_scalar_fields(
                        old_exchange.user_message
                    )
                    new_exchange.user_message = new_user_message

                for old_reply in old_exchange.agent_replies:
                    new_reply = self._clone_scalar_fields(old_reply)
                    new_exchange.agent_replies.append(new_reply)

                new_chat.exchanges.append(new_exchange)

                if old_exchange.id == last_exchange_id:
                    required_last_exchange_found = True
                    break

            if not required_last_exchange_found:
                raise NonexistentExchangeError(last_exchange_id or 0)

            db.add(new_chat)
            db.commit()

            self._event_bus.publish(
                ChatCreatedEvent(user_id=new_chat.owner_id, chat_id=new_chat.id)
            )
            return new_chat.id

    def send_markdown_message_to_user_chat(
        self, user_id: int, chat_id: int, from_agent_id: Optional[int], markdown: str
    ) -> int:
        """Sends a Markdown message to the given Chat and returns the id of the created Exchange."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)
            new_exchange = ChatExchange(
                timestamp=datetime.now(tz=UTC),
            )
            msg = ChatMessageMarkdown(timestamp=datetime.now(tz=UTC), markdown=markdown)

            chat.exchanges.append(new_exchange)
            db.flush()

            if from_agent_id is None:
                new_exchange.user_message = msg
                msg.sending_user = chat.owner

                triggered_event_ids = self._trigger.receive_chat_message(
                    receiver=chat.receiver,
                    message=markdown,
                    chat_id=chat_id,
                    exchange_id=new_exchange.id,
                )
                for event_id in triggered_event_ids:
                    event = db.scalar(select(Event).where(Event.id == event_id))

                    if event is not None:
                        new_exchange.triggered_chat_events.append(event)
            else:
                # TODO: Change the method signature so from_agent_id is from_monologue_id - then it is possible
                # to add event metadata to this exchange - right now, if an agent sends a message the responsible
                # monologue is not shown.
                agent = db.scalar(select(Agent).where(Agent.id == from_agent_id))
                msg.sending_agent = agent
                new_exchange.agent_replies.append(msg)
                new_exchange.triggered_chat_events = []

            chat.modified_at = datetime.now(tz=UTC)
            db.commit()

            self._event_bus.publish(
                ChatExchangeCreatedEvent(
                    user_id=user_id, chat_id=chat_id, exchange_id=new_exchange.id
                )
            )
            self._event_bus.publish(
                ChatMessageSentEvent(
                    user_id=user_id, chat_id=chat_id, exchange_id=new_exchange.id
                )
            )
            return new_exchange.id

    def send_choice_message_to_user_chat(
        self,
        user_id: int,
        chat_id: int,
        from_agent_id: Optional[int],
        prompt: str,
        choices: List[Any],
    ) -> Tuple[int, int]:
        """Sends a Choice message to the given Chat and returns the id of the created Exchange and the query ID of the choice."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)
            new_exchange = ChatExchange(
                timestamp=datetime.now(tz=UTC),
            )

            choices = [ChoiceMessageOption(value=x) for x in choices]
            msg = ChatMessageChoicePrompt(
                timestamp=datetime.now(tz=UTC), prompt=prompt, choices=choices
            )

            if from_agent_id is None:
                new_exchange.user_message = msg
                msg.sending_user = chat.owner
            else:
                # TODO: Change the method signature so from_agent_id is from_monologue_id - then it is possible
                # to add event metadata to this exchange - right now, if an agent sends a message the responsible
                # monologue is not shown.
                agent = db.scalar(select(Agent).where(Agent.id == from_agent_id))
                msg.sending_agent = agent
                new_exchange.agent_replies.append(msg)
                new_exchange.triggered_chat_events = []

            chat.modified_at = datetime.now(tz=UTC)
            chat.exchanges.append(new_exchange)
            db.commit()

            self._event_bus.publish(
                ChatExchangeCreatedEvent(
                    user_id=user_id, chat_id=chat_id, exchange_id=new_exchange.id
                )
            )
            self._event_bus.publish(
                ChatMessageSentEvent(
                    user_id=user_id, chat_id=chat_id, exchange_id=new_exchange.id
                )
            )
            return new_exchange.id, msg.id

    def send_markdown_reply_to_user_exchange(
        self,
        user_id: int,
        exchange_id: int,
        from_agent_id: Optional[int],
        markdown: str,
    ):
        """Sends a Markdown reply to the given Exchange."""
        with self._db.session() as db:
            exchange = self._load_user_exchange(db, user_id, exchange_id)
            msg = ChatMessageMarkdown(timestamp=datetime.now(tz=UTC), markdown=markdown)

            if from_agent_id is not None:
                agent = db.scalar(select(Agent).where(Agent.id == from_agent_id))
                msg.sending_agent = agent

            exchange.agent_replies.append(msg)
            exchange.chat.modified_at = datetime.now(tz=UTC)
            db.commit()

            self._event_bus.publish(
                ChatMessageSentEvent(
                    user_id=user_id,
                    chat_id=exchange.chat.id,
                    exchange_id=exchange.id,
                    reply_id=msg.id,
                )
            )

    def send_choice_reply_to_user_exchange(
        self,
        user_id: int,
        exchange_id: int,
        from_agent_id: Optional[int],
        prompt: str,
        choices: List[Any],
    ) -> int:
        """Sends a Choice reply to the given Exchange and returns the query ID of the choice."""
        with self._db.session() as db:
            exchange = self._load_user_exchange(db, user_id, exchange_id)
            choices = [ChoiceMessageOption(value=x) for x in choices]
            msg = ChatMessageChoicePrompt(
                timestamp=datetime.now(tz=UTC), prompt=prompt, choices=choices
            )

            if from_agent_id is not None:
                agent = db.scalar(select(Agent).where(Agent.id == from_agent_id))
                msg.sending_agent = agent

            exchange.agent_replies.append(msg)
            exchange.chat.modified_at = datetime.now(tz=UTC)
            db.commit()

            self._event_bus.publish(
                ChatMessageSentEvent(
                    user_id=user_id,
                    chat_id=exchange.chat.id,
                    exchange_id=exchange.id,
                    reply_id=msg.id,
                )
            )

            return msg.id

    def get_user_chat_exchanges_after(
        self, user_id: int, chat_id: int, after: int
    ) -> List[ChatExchange]:
        """Gets user chat exchanges created after the given point in time."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)
            after_dt = datetime.fromtimestamp(after + 1, tz=UTC)
            res = (
                db.scalars(
                    select(ChatExchange)
                    .options(
                        # Eager load Markdown contents
                        joinedload(
                            ChatExchange.user_message.of_type(ChatMessageMarkdown)
                        ).options(undefer(ChatMessageMarkdown.markdown)),
                        # Eager load ChoicePrompt options
                        joinedload(
                            ChatExchange.user_message.of_type(ChatMessageChoicePrompt)
                        )
                        .options(undefer(ChatMessageChoicePrompt.prompt))
                        .joinedload(ChatMessageChoicePrompt.choices)
                        .options(undefer(ChoiceMessageOption.value)),
                        # Eager load sending user and agent
                        joinedload(ChatExchange.user_message).options(
                            joinedload(ChatMessage.sending_user),
                            joinedload(ChatMessage.sending_agent),
                        ),
                        # Eager load triggered chat events and their monologues
                        joinedload(ChatExchange.triggered_chat_events).joinedload(
                            Event.monologues
                        ),
                    )
                    .where(
                        ChatExchange.chat_id == chat.id,
                        ChatExchange.timestamp > after_dt,
                    )
                    .order_by(ChatExchange.timestamp.asc())
                )
                .unique()
                .all()
            )

            return res

    def get_user_exchange_replies_after(
        self, user_id: int, exchange_id: int, after: int
    ) -> List[ChatMessage]:
        """Gets replies to an Exchange sent after the given point in time."""
        with self._db.session() as db:
            exchange = self._load_user_exchange(db, user_id, exchange_id)
            after_dt = datetime.fromtimestamp(after + 1, tz=UTC)

            ChatMessagePoly = with_polymorphic(
                base=ChatMessage, classes=[ChatMessageMarkdown, ChatMessageChoicePrompt]
            )
            res = (
                db.scalars(
                    select(ChatMessagePoly)
                    .options(
                        # Eager load Markdown contents
                        undefer(ChatMessagePoly.ChatMessageMarkdown.markdown),
                        # Eager load ChoicePrompt choices
                        joinedload(
                            ChatMessagePoly.ChatMessageChoicePrompt.choices
                        ).options(undefer(ChoiceMessageOption.value)),
                        # Eager load sending user and agent
                        joinedload(ChatMessagePoly.sending_user),
                        joinedload(ChatMessagePoly.sending_agent),
                    )
                    .where(
                        ChatMessage.reply_exchange_id == exchange.id,
                        ChatMessage.timestamp > after_dt,
                    )
                    .order_by(ChatMessage.timestamp.asc())
                )
                .unique()
                .all()
            )

            return res

    def update_user_chat_options(
        self, user_id: int, chat_id: int, options: "ChatOptionsDiff"
    ):
        """Updates the options of the given Chat."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)

            if options.receiver is not None:
                chat.receiver = options.receiver

            if options.enabled_action_ids is not None:
                chat.allowed_actions = []

                for action_id in options.enabled_action_ids:
                    action = db.scalar(
                        select(Action)
                        .join(User.allowed_actions)
                        .where(Action.id == action_id, User.id == user_id)
                    )

                    if action is not None:
                        chat.allowed_actions.append(action)

            db.commit()

            self._event_bus.publish(
                ChatOptionsSetEvent(user_id=chat.owner_id, chat_id=chat.id)
            )

    def set_user_chat_summary(self, user_id: int, chat_id: int, summary: str):
        """Sets the summary of the given Chat."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)
            chat.summary = summary
            db.commit()

            self._event_bus.publish(
                ChatSummarySetEvent(
                    user_id=chat.owner_id, chat_id=chat.id, summary=chat.summary
                )
            )

    def get_user_chat_messages(self, user_id: int, chat_id: int) -> List[ChatMessage]:
        """Returns all the messages sent in the current chat (flattened from all exchanges)."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)

            ChatMessagePoly = with_polymorphic(
                base=ChatMessage, classes=[ChatMessageMarkdown, ChatMessageChoicePrompt]
            )
            res = (
                db.scalars(
                    select(ChatMessagePoly)
                    .join(
                        ChatExchange,
                        or_(
                            ChatExchange.id == ChatMessage.usermsg_exchange_id,
                            ChatExchange.id == ChatMessage.reply_exchange_id,
                        ),
                    )
                    .join(ChatExchange.chat)
                    .options(
                        # Eager load Markdown contents
                        undefer(ChatMessagePoly.ChatMessageMarkdown.markdown),
                        # Eager load ChoicePrompt choices
                        joinedload(
                            ChatMessagePoly.ChatMessageChoicePrompt.choices
                        ).options(undefer(ChoiceMessageOption.value)),
                        # Eager load sending user and agent
                        joinedload(ChatMessagePoly.sending_user),
                        joinedload(ChatMessagePoly.sending_agent),
                    )
                    .where(Chat.id == chat_id)
                    .order_by(ChatMessage.timestamp.asc())
                )
                .unique()
                .all()
            )

            return res

    def get_user_query_answer(self, user_id: int, message_id: int) -> Any:
        """Returns the user's answer to the given query."""
        with self._db.session() as db:
            msg = self._load_user_message(db, user_id, message_id)

            if not isinstance(msg, ChatMessageChoicePrompt):
                raise NonexistentMessageError(message_id)

            return msg.answer

    def set_user_query_answer(self, user_id: int, message_id: int, answer: Any):
        """Sets the answer to the given query."""
        with self._db.session() as db:
            msg = self._load_user_message(db, user_id, message_id)

            if not isinstance(msg, ChatMessageChoicePrompt):
                raise NonexistentMessageError(message_id)

            if msg.answer is not None:
                raise QueryAlreadyAnsweredError(message_id)

            msg.answer = answer
            db.commit()

            self._event_bus.publish(
                QueryAnsweredEvent(user_id=user_id, query_id=msg.id, answer=msg.answer)
            )

    # TODO: Factor this out into a utility module and unit test it
    def _clone_scalar_fields(self, orm_obj):
        """Clones an SQLAlchemy ORM object, but only the non-primary-key scalar fields."""
        cls = type(orm_obj)
        res = cls()

        for col in orm_obj.__mapper__.columns:
            if not col.primary_key:
                setattr(res, col.key, getattr(orm_obj, col.key))

        return res

    def _load_user_chat(self, db: Session, user_id: int, chat_id: int):
        res = db.scalar(
            select(Chat).where(Chat.id == chat_id, Chat.owner_id == user_id)
        )

        if res is None:
            raise NonexistentChatError(chat_id)

        return res

    def _load_user_exchange(self, db: Session, user_id: int, exchange_id: int):
        res = db.scalar(
            select(ChatExchange)
            .join(ChatExchange.chat)
            .where(ChatExchange.id == exchange_id, Chat.owner_id == user_id)
        )

        if res is None:
            raise NonexistentExchangeError(exchange_id)

        return res

    def _load_user_message(self, db: Session, user_id: int, message_id: int):
        res = db.scalar(
            select(ChatMessage)
            .join(
                ChatExchange,
                or_(
                    ChatExchange.id == ChatMessage.usermsg_exchange_id,
                    ChatExchange.id == ChatMessage.reply_exchange_id,
                ),
            )
            .join(ChatExchange.chat)
            .where(Chat.owner_id == user_id, ChatMessage.id == message_id)
        )

        if res is None:
            raise NonexistentMessageError(message_id)

        return res


class ChatOptionsDiff(BaseModel):
    receiver: Optional[str] = None
    enabled_action_ids: Optional[List[int]] = None


@dataclass
class ChatCreatedEvent(event_bus.Event):
    user_id: int
    chat_id: int


@dataclass
class ChatDeletedEvent(event_bus.Event):
    user_id: int
    chat_id: int


@dataclass
class ChatExchangeCreatedEvent(event_bus.Event):
    user_id: int
    chat_id: int
    exchange_id: int


@dataclass
class ChatMessageSentEvent(event_bus.Event):
    user_id: int
    chat_id: Optional[int] = None
    exchange_id: Optional[int] = None
    reply_id: Optional[int] = None


@dataclass
class ChatSummarySetEvent(event_bus.Event):
    user_id: int
    chat_id: int
    summary: str


@dataclass
class ChatOptionsSetEvent(event_bus.Event):
    user_id: int
    chat_id: int


@dataclass
class QueryAnsweredEvent(event_bus.Event):
    user_id: int
    query_id: int
    answer: Any


class CannotCreateChatForNonexistentUserError(Exception):
    def __init__(self, id: int):
        super().__init__(f"cannot create chat for nonexistent user with ID {id}")


class NonexistentChatError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent chat with ID {id}")


class NonexistentExchangeError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent exchange with ID {id}")


class NonexistentMessageError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent message with ID {id}")


class QueryAlreadyAnsweredError(Exception):
    def __init__(self, id: int):
        super().__init__(f"query message with ID {id} was already answered")
