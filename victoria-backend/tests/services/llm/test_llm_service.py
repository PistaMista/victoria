import pytest

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

def test_llm_service_can_add_a_new_ollama_connection(db_serv):
    assert False

def test_llm_service_imports_models_from_added_ollama_connection():
    assert False

def test_llm_service_fails_to_add_ollama_connection_on_ollama_communication_failure():
    assert False

def test_llm_service_imports_models_from_existing_connections_on_startup():
    assert False

def test_llm_service_overrides_models_in_database_with_models_from_existing_connection():
    assert False
    
def test_llm_service_keeps_models_in_database_on_ollama_communication_failure():
    assert False

def test_llm_service_can_remove_an_ollama_connection():
    assert False

def test_llm_service_removes_models_imported_from_a_removed_connection():
    assert False

def test_llm_service_calls_ollama_api_correctly_for_chat_completion():
    assert False
    
def test_llm_service_does_not_catch_http_exceptions_during_chat_completion():
    assert False

def test_llm_service_throws_when_using_nonexistent_model_for_chat_completion():
    assert False
    
def test_llm_service_throws_when_using_disabled_model_for_chat_completion():
    assert False
