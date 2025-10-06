import pytest
from unittest import mock
from app.services.db import DatabaseService
from app.model.user import User, Role
from app.model.agent import Agent
from app.model.action import Action
from app.model.action_repository import ActionRepository
from sqlalchemy import select

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

def test_agent_service_can_get_all_agents_owned_by_user(db_serv, db_session):
    assert False

def test_agent_service_returns_empty_list_when_getting_agents_for_nonexistent_user(db_serv, db_session):
    assert False

def test_agent_service_can_find_if_agent_has_any_running_monologues(db_serv, db_session):
    assert False

def test_agent_service_can_create_a_new_agent_with_valid_settings(db_serv, db_session):
    assert False

def test_agent_service_throws_when_creating_agent_for_nonexistent_user(db_serv, db_session):
    assert False

def test_agent_service_throws_when_creating_agent_with_nonexistent_actions(db_serv, db_session):
    assert False

def test_agent_service_throws_when_creating_agent_with_nonexistent_triggers(db_serv, db_session):
    assert False

def test_agent_service_throws_when_creating_agent_with_nonexistent_model(db_serv, db_session):
    assert False

def test_agent_service_can_do_simple_agent_update_with_valid_settings(db_serv, db_session):
    assert False

def test_agent_service_can_get_an_agent_by_id_including_actions_and_triggers(db_serv, db_session):
    assert False

def test_agent_service_can_do_complex_agent_update_with_valid_settings(db_serv, db_session):
    assert False

def test_agent_service_throws_when_updating_agent_with_nonexistent_actions(db_serv, db_session):
    assert False

def test_agent_service_throws_when_updating_agent_with_nonexistent_triggers(db_serv, db_session):
    assert False

def test_agent_service_throws_when_updating_agent_with_nonexistent_model(db_serv, db_session):
    assert False

def test_agent_service_can_remove_agent(db_serv, db_session):
    assert False

def test_agent_service_throws_when_trying_to_manipulate_nonexistent_agent(db_serv, db_session):
    assert False

def test_agent_service_throws_when_trying_to_manipulate_existing_agent_with_nonexistent_user_id(db_serv, db_session):
    assert False

def test_agent_service_throws_when_trying_to_manipulate_existing_agent_with_non_owner(db_serv, db_session):
    assert False
