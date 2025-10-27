from pydantic import BaseModel
from typing import Optional, List, Any, Tuple
from enum import Enum
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from app.services.db import DatabaseService
from app.services.trigger import TriggerService
from app.model.user import User
from app.model.chat import Chat
from app.model.chat_exchange import ChatExchange
from app.model.chat_message import ChatMessage
from datetime import datetime, UTC

class ChatSortMode(Enum):
    LONGEST = 0
    RECENT = 1

class ChatService:
    def __init__(
        self,
        database_service: DatabaseService,
        trigger_service: TriggerService
    ):
        self._db: DatabaseService = database_service

    def get_user_chats(self, user_id: int, sort_by: ChatSortMode = ChatSortMode.RECENT, search_query: Optional[str] = None) -> List[Chat]:
        """Gets all chats of the given User."""
        with self._db.session() as db:
            stmt = select(Chat).where(Chat.owner_id == user_id)

            if search_query is not None:
                stmt = stmt.where(or_(
                    func.lower(Chat.title).like(f"%{search_query.lower()}%"),
                    func.lower(Chat.summary).like(f"%{search_query.lower()}%")
                ))

            match sort_by:
                case ChatSortMode.RECENT:
                    stmt = stmt.order_by(Chat.modified_at.desc())
                case ChatSortMode.LONGEST:
                    stmt = (
                        stmt
                        .outerjoin(Chat.exchanges)
                        .group_by(Chat.id)
                        .order_by(func.count(ChatExchange.id).desc())
                    )

            res = db.scalars(stmt).all()
            return res


    def create_user_chat(self, user_id: int) -> int:
        """Creates a new blank chat for a user and returns its id."""
        with self._db.session() as db:
            user = db.scalar(
                select(User).where(User.id == user_id)
            )

            if user is None:
                raise CannotCreateChatForNonexistentUserError(user_id)

            new_chat = Chat(
                title="Untitled",
                summary="No summary",
                receiver="",
                created_at=datetime.now(tz=UTC),
                modified_at=datetime.now(tz=UTC),
                owner=user
            )

            db.add(new_chat)
            db.commit()

            return new_chat.id

    def get_user_chat(self, user_id: int, chat_id: int) -> Chat:
        """Gets a User's chat."""
        with self._db.session() as db:
            chat = self._load_user_chat(db, user_id, chat_id)

            db.refresh(chat, ["allowed_actions"])
            return chat

    def get_user_chat_receivers(self, user_id: int) -> List[str]:
        """Gets all the valid chat receivers for the given User."""
        pass

    def remove_user_chat(self, user_id: int, chat_id: int):
        """Deletes the given Chat."""
        pass

    def duplicate_user_chat(self, user_id: int, chat_id: int, last_exchange_id: Optional[int] = None) -> int:
        """Duplicates the given Chat up to the given Exchange and returns the new id."""
        pass

    def send_markdown_message_to_user_chat(self, user_id: int, chat_id: int, from_agent_id: Optional[int], markdown: str) -> int:
        """Sends a Markdown message to the given Chat and returns the id of the created Exchange."""
        pass

    def send_choice_message_to_user_chat(self, user_id: int, chat_id: int, from_agent_id: Optional[int], prompt: str, choices: List[Any]) -> Tuple[int, int]:
        """Sends a Choice message to the given Chat and returns the id of the created Exchange and the query ID of the choice."""
        pass

    def send_markdown_reply_to_user_exchange(self, user_id: int, exchange_id: int, from_agent_id: Optional[int], markdown: str):
        """Sends a Markdown reply to the given Exchange."""
        pass

    def send_choice_reply_to_user_exchange(self, user_id: int, exchange_id: int, from_agent_id: Optional[int], prompt: str, choices: List[Any]) -> int:
        """Sends a Choice reply to the given Exchange and returns the query ID of the choice."""
        pass

    def get_user_chat_exchanges_after(self, user_id: int, chat_id: int, after: int) -> List[ChatExchange]:
        """Gets user chat exchanges created after the given point in time."""
        pass

    def get_user_exchange_replies_after(self, user_id: int, exchange_id: int, after: int) -> List[ChatMessage]:
        """Gets replies to an Exchange sent after the given point in time."""
        pass

    def update_user_chat_options(self, user_id: int, chat_id: int, options: "ChatOptionsDiff"):
        """Updates the options of the given Chat."""
        pass

    def set_user_chat_summary(self, user_id: int, chat_id: int, summary: str):
        """Sets the summary of the given Chat."""
        pass

    def get_user_chat_messages(self, user_id: int, chat_id: int) -> List[ChatMessage]:
        """Returns all the messages sent in the current chat (flattened from all exchanges)."""
        pass

    def get_user_query_answer(self, user_id: int, message_id: int) -> Any:
        """Returns the user's answer to the given query."""
        pass

    def set_user_query_answer(self, user_id: int, message_id: int, answer: Any):
        """Sets the answer to the given query."""
        pass

    def _load_user_chat(self, db: Session, user_id: int, chat_id: int):
        res = db.scalar(
            select(Chat)
            .where(Chat.id == chat_id, Chat.owner_id == user_id)
        )

        if res is None:
            raise NonexistentChatError(chat_id)

        return res


class ChatOptionsDiff(BaseModel):
    receiver: Optional[str] = None
    enabled_action_ids: Optional[List[int]] = None

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
