import pytest
from unittest import mock
from app.services.db import DatabaseService
from app.services.chat import ChatService, NonexistentChatError, NonexistentExchangeError, NonexistentMessageError, QueryAlreadyAnsweredError

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

def test_chat_service_can_get_all_chats_owned_by_user(db_serv, db_session):
    assert False

def test_chat_service_returns_empty_list_when_getting_chats_for_nonexistent_user(db_serv, db_session):
    assert False

def test_chat_service_can_create_new_blank_chat_for_user(db_serv, db_session):
    assert False

# FIXME: Define the behavior for creating new chats properly!
def test_chat_service_behavior_is_undefined_when_creating_new_chat_for_nonexistent_user(db_serv, db_session):
    assert False

def test_chat_service_can_get_chat_by_id(db_serv, db_session):
    assert False

def test_chat_service_can_get_chat_receivers_of_user(db_serv, db_session):
    assert False

def test_chat_service_can_remove_user_chat_including_exchanges_and_messages(db_serv, db_session):
    assert False

def test_chat_service_can_duplicate_entire_user_chat(db_serv, db_session):
    assert False

def test_chat_service_can_duplicate_user_chat_up_to_certain_exchange(db_serv, db_session):
    assert False

def test_chat_service_throws_when_invalid_last_exchange_id_specified_during_duplicate(db_serv, db_session):
    assert False

def test_chat_service_can_send_markdown_message_to_user_chat_from_user(db_serv, db_session):
    assert False

def test_chat_service_can_send_markdown_message_to_user_chat_from_agent(db_serv, db_session):
    assert False

def test_chat_service_can_send_choice_message_to_user_chat_from_agent(db_serv, db_session):
    assert False

def test_chat_service_can_send_markdown_reply_to_user_exchange_from_agent(db_serv, db_session):
    assert False

def test_chat_service_can_send_choice_reply_to_user_exchange_from_agent(db_serv, db_session):
    assert False

def test_chat_service_leaves_agent_field_blank_for_sent_messages_for_nonexistent_agent_ids(db_serv, db_session):
    assert False

def test_chat_service_can_get_exchanges_after_timestamp_including_user_message(db_serv, db_session):
    assert False

def test_chat_service_can_get_exchange_replies_after_timestamp(db_serv, db_session):
    assert False

def test_chat_service_can_set_user_chat_summary(db_serv, db_session):
    assert False

def test_chat_service_can_get_all_messages_from_user_chat_flattened(db_serv, db_session):
    assert False

def test_chat_service_can_get_answered_query_answer_of_choice_message(db_serv, db_session):
    assert False

def test_chat_service_returns_None_when_getting_answer_for_unanswered_query_of_choice_message(db_serv, db_session):
    assert False

def test_chat_service_can_set_unanswered_query_answer(db_serv, db_session):
    assert False

def test_chat_service_throws_when_setting_answer_for_answered_query(db_serv, db_session):
    assert False

def test_chat_service_throws_when_trying_to_manipulate_nonexistent_chat(db_serv, db_session):
    assert False

def test_chat_service_throws_when_trying_to_manipulate_nonexistent_exchange(db_serv, db_session):
    assert False

def test_chat_service_throws_when_trying_to_manipulate_nonexistent_message(db_serv, db_session):
    assert False
