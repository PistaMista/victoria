import pytest
from unittest import mock
from app.services.llm import LLMService, SystemMessage, UserMessage, AssistantMessage, OllamaCommunicationError, NonexistentConnectionError, NonexistentModelError, DisabledModelError
from app.services.db import DatabaseService
from app.model.llm_connection import LLMConnection, OllamaConnection
from app.model.language_model import LanguageModel
from sqlalchemy import select
from requests import HTTPError, ConnectionError


@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

@mock.patch('app.services.llm.requests.get')
def test_llm_service_can_add_a_new_ollama_connection(mock_get, db_serv, db_session):
    # Arrange
    serv = LLMService(
        database_service=db_serv
    )
    
    # Act
    serv.add_ollama_connection(
        name="Homelab",
        url="http://localhost:11434"
    )
    
    # Assert
    connections = db_session.scalars(
        select(LLMConnection)
    )
    
    assert len(connections) == 1
    assert connections[0].name == "Homelab"
    assert connections[0].url == "http://localhost:11434"

@mock.patch('app.services.llm.requests.get')
def test_llm_service_imports_models_from_added_ollama_connection(mock_get, db_serv, db_session):
    # Arrange
    mock_res = mock_get.return_value
    mock_res.status_code == 200
    mock_res.json.return_value = {
      "models": [
        {
          "name": "deepseek-r1:latest",
          "model": "deepseek-r1:latest",
          "modified_at": "2025-05-10T08:06:48.639712648-07:00",
          "size": 4683075271,
          "digest": "0a8c266910232fd3291e71e5ba1e058cc5af9d411192cf88b6d30e92b6e73163",
          "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "qwen2",
            "families": [
              "qwen2"
            ],
            "parameter_size": "7.6B",
            "quantization_level": "Q4_K_M"
          }
        },
        {
          "name": "llama3.2:latest",
          "model": "llama3.2:latest",
          "modified_at": "2025-05-04T17:37:44.706015396-07:00",
          "size": 2019393189,
          "digest": "a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72",
          "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "llama",
            "families": [
              "llama"
            ],
            "parameter_size": "3.2B",
            "quantization_level": "Q4_K_M"
          }
        }
      ]
    }        

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act
    serv.add_ollama_connection(
        name="Homelab",
        url="http://localhost:11434"
    )
    
    # Assert
    mock_get.assert_called_once_with("http://localhost:11434/api/tags")
    connection = db_session.scalars(
        select(LLMConnection)
    ).first()
    
    models = db_session.scalars(
        select(LanguageModel)
        .order_by(LanguageModel.name)
    )
    
    assert len(models) == 2

    assert models[0].name == "deepseek-r1:latest"
    assert models[0].enabled
    assert models[0].connection == connection

    assert models[1].name == "llama3.2:latest"
    assert models[1].enabled
    assert models[1].connection == connection
    
@mock.patch('app.services.llm.requests.get')
def test_llm_service_fails_to_add_ollama_connection_on_ollama_error_status_code(mock_get, db_serv, db_session):
    # Arrange
    mock_res = mock_get.return_value
    mock_res.status_code == 400
    mock_res.raise_for_status.side_effect = HTTPError()
    serv = LLMService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(OllamaCommunicationError):
        serv.add_ollama_connection(
            name="Homelab",
            url="http://localhost:11434"
        )
        
    connections = db_session.scalars(
        select(LLMConnection)
    )
    models = db_session.scalars(
        select(LanguageModel)
    )
    
    assert connections.first() is None
    assert models.first() is None

@mock.patch('app.services.llm.requests.get')
def test_llm_service_fails_to_add_ollama_connection_on_ollama_server_connection_error(mock_get, db_serv, db_session):
    # Arrange
    mock_get.side_effect = ConnectionError()
    serv = LLMService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(OllamaCommunicationError):
        serv.add_ollama_connection(
            name="Homelab",
            url="http://localhost:11434"
        )
        
    connections = db_session.scalars(
        select(LLMConnection)
    )
    models = db_session.scalars(
        select(LanguageModel)
    )
    
    assert connections.first() is None
    assert models.first() is None

@mock.patch('app.services.llm.requests.get')
def test_llm_service_imports_models_from_existing_connections_on_startup(mock_get, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        name="Megacenter",
        url="http://www.megacenter.com:11434"
    )
    
    db_session.add(connection)
    db_session.commit()

    mock_res = mock_get.return_value
    mock_res.status_code == 200
    mock_res.json.return_value = {
      "models": [
        {
          "name": "deepseek-r1:latest",
          "model": "deepseek-r1:latest",
          "modified_at": "2025-05-10T08:06:48.639712648-07:00",
          "size": 4683075271,
          "digest": "0a8c266910232fd3291e71e5ba1e058cc5af9d411192cf88b6d30e92b6e73163",
          "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "qwen2",
            "families": [
              "qwen2"
            ],
            "parameter_size": "7.6B",
            "quantization_level": "Q4_K_M"
          }
        },
        {
          "name": "llama3.2:latest",
          "model": "llama3.2:latest",
          "modified_at": "2025-05-04T17:37:44.706015396-07:00",
          "size": 2019393189,
          "digest": "a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72",
          "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "llama",
            "families": [
              "llama"
            ],
            "parameter_size": "3.2B",
            "quantization_level": "Q4_K_M"
          }
        }
      ]
    }        
    
    # Act
    serv = LLMService(
        database_service=db_serv
    )
    
    # Assert
    mock_get.assert_called_once_with("http://localhost:11434/api/tags")
    models = db_session.scalars(
        select(LanguageModel)
        .order_by(LanguageModel.name)
    )
    
    assert len(models) == 2

    assert models[0].name == "deepseek-r1:latest"
    assert models[0].enabled
    assert models[0].connection == connection

    assert models[1].name == "llama3.2:latest"
    assert models[1].enabled
    assert models[1].connection == connection
    
    
@mock.patch('app.services.llm.requests.get')
def test_llm_service_overrides_models_in_database_with_models_from_existing_connection(mock_get, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        name="gemma3:12b",
        enabled=True,
        connection=connection
    )
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    mock_res = mock_get.return_value
    mock_res.status_code == 200
    mock_res.json.return_value = {
      "models": [
        {
          "name": "deepseek-r1:latest",
          "model": "deepseek-r1:latest",
          "modified_at": "2025-05-10T08:06:48.639712648-07:00",
          "size": 4683075271,
          "digest": "0a8c266910232fd3291e71e5ba1e058cc5af9d411192cf88b6d30e92b6e73163",
          "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "qwen2",
            "families": [
              "qwen2"
            ],
            "parameter_size": "7.6B",
            "quantization_level": "Q4_K_M"
          }
        },
        {
          "name": "llama3.2:latest",
          "model": "llama3.2:latest",
          "modified_at": "2025-05-04T17:37:44.706015396-07:00",
          "size": 2019393189,
          "digest": "a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72",
          "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "llama",
            "families": [
              "llama"
            ],
            "parameter_size": "3.2B",
            "quantization_level": "Q4_K_M"
          }
        }
      ]
    }        
    
    # Act
    serv = LLMService(
        database_service=db_serv
    )
    
    # Assert
    mock_get.assert_called_once_with("http://localhost:11434/api/tags")
    models = db_session.scalars(
        select(LanguageModel)
        .order_by(LanguageModel.name)
    )
    
    assert len(models) == 2

    assert models[0].name == "deepseek-r1:latest"
    assert models[0].connection == connection

    assert models[1].name == "llama3.2:latest"
    assert models[1].connection == connection
    
@mock.patch('app.services.llm.requests.get')
def test_llm_service_keeps_models_in_database_on_ollama_communication_failure(mock_get, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        name="gemma3:12b",
        enabled=True,
        connection=connection
    )
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    mock_get.side_effect = ConnectionError()
    
    # Act
    serv = LLMService(
        database_service=db_serv
    )
    
    # Assert
    mock_get.assert_called_once_with("http://localhost:11434/api/tags")
    models = db_session.scalars(
        select(LanguageModel)
        .order_by(LanguageModel.name)
    )
    
    assert len(models) == 1

    assert models[0].name == "gemma3:12b"
    assert models[0].connection == connection

@mock.patch('app.services.llm.requests.get')
def test_llm_service_can_remove_an_ollama_connection(mock_get, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        id=10,
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        name="gemma3:12b",
        enabled=True,
        connection=connection
    )
    
    mock_get.side_effect = ConnectionError()
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act
    serv.remove_ollama_connection(10)
    
    # Assert
    connections = db_session.scalars(
        select(LLMConnection)
    )
    
    assert connections.first() is None

@mock.patch('app.services.llm.requests.get')
def test_llm_service_throws_when_removing_nonexistent_connection(mock_get, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        id=10,
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        name="gemma3:12b",
        enabled=True,
        connection=connection
    )
    
    mock_get.side_effect = ConnectionError()
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(NonexistentConnectionError):
        serv.remove_ollama_connection(15)
    
    connections = db_session.scalars(
        select(LLMConnection)
    )
    
    assert connections.first() == connection
    
    
@mock.patch('app.services.llm.requests.get')
def test_llm_service_removes_models_imported_from_a_removed_connection(mock_get, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        id=10,
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        name="gemma3:12b",
        enabled=True,
        connection=connection
    )
    
    mock_get.side_effect = ConnectionError()
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act
    serv.remove_ollama_connection(10)
    
    # Assert
    models = db_session.scalars(
        select(LanguageModel)
    )
    
    assert models.first() is None

@mock.patch('app.services.llm.requests.get')
@mock.patch('app.services.llm.requests.post')
def test_llm_service_uses_ollama_api_correctly_for_chat_completion(mock_get, mock_post, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        id=10,
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        id=3,
        enabled=True,
        name="gemma3:12b",
        connection=connection
    )
    
    mock_get.side_effect = ConnectionError()
    mock_post_res = mock_post.return_value
    mock_post_res.status_code = 200
    mock_post_res.json.return_value = {
      "model": "gemma3:12b",
      "created_at": "2023-12-12T14:13:43.416799Z",
      "message": {
        "role": "assistant",
        "content": "Here is a recipe..."
      },
      "done": True,
      "total_duration": 5191566416,
      "load_duration": 2154458,
      "prompt_eval_count": 26,
      "prompt_eval_duration": 383809000,
      "eval_count": 298,
      "eval_duration": 4799921000
    }
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act
    res = serv.get_chat_completion(3, [
        SystemMessage("YOU ARE THE ONE NEO!"),
        UserMessage("Hello there!"),
        AssistantMessage("What can I help you with?"),
        UserMessage("Give me a recipe for fish and chips.")
    ])
    
    # Assert
    mock_post.assert_called_once_with(
        "http://www.megacenter.com:11434/api/chat",
        json={
            "model": "gemma3:12b",
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": "YOU ARE THE ONE NEO!"
                },
                {
                    "role": "user",
                    "content": "Hello there!"
                },
                {
                    "role": "assistant",
                    "content": "What can I help you with?"
                },
                {
                    "role": "user",
                    "content": "Give me a recipe for fish and chips"
                }
            ]
        }
    )
    assert res == AssistantMessage("Here is a recipe...")

    
@mock.patch('app.services.llm.requests.get')
@mock.patch('app.services.llm.requests.post')
def test_llm_service_throws_on_communication_failure_during_chat_completion(mock_get, mock_post, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        id=10,
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        id=3,
        enabled=True,
        name="gemma3:12b",
        connection=connection
    )
    
    mock_get.side_effect = ConnectionError()
    mock_post.side_effect = ConnectionError()
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(OllamaCommunicationError):
        serv.get_chat_completion(3, [
            SystemMessage("YOU ARE THE ONE NEO!"),
            UserMessage("Hello there!"),
            AssistantMessage("What can I help you with?"),
            UserMessage("Give me a recipe for fish and chips.")
        ])


@mock.patch('app.services.llm.requests.get')
@mock.patch('app.services.llm.requests.post')
def test_llm_service_throws_when_using_nonexistent_model_for_chat_completion(mock_get, mock_post, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        id=10,
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        id=3,
        enabled=True,
        name="gemma3:12b",
        connection=connection
    )
    
    mock_get.side_effect = ConnectionError()
    mock_post_res = mock_post.return_value
    mock_post_res.status_code = 200
    mock_post_res.json.return_value = {
      "model": "gemma3:12b",
      "created_at": "2023-12-12T14:13:43.416799Z",
      "message": {
        "role": "assistant",
        "content": "Here is a recipe..."
      },
      "done": True,
      "total_duration": 5191566416,
      "load_duration": 2154458,
      "prompt_eval_count": 26,
      "prompt_eval_duration": 383809000,
      "eval_count": 298,
      "eval_duration": 4799921000
    }
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(NonexistentModelError):
        serv.get_chat_completion(42, [
            SystemMessage("YOU ARE THE ONE NEO!"),
            UserMessage("Hello there!"),
            AssistantMessage("What can I help you with?"),
            UserMessage("Give me a recipe for fish and chips.")
        ])
    
@mock.patch('app.services.llm.requests.get')
@mock.patch('app.services.llm.requests.post')
def test_llm_service_throws_when_using_disabled_model_for_chat_completion(mock_get, mock_post, db_serv, db_session):
    # Arrange
    connection = OllamaConnection(
        id=10,
        name="Megacenter",
        url="http://www.megacenter.com:11434"        
    )
    model = LanguageModel(
        id=3,
        enabled=False,
        name="gemma3:12b",
        connection=connection
    )
    
    mock_get.side_effect = ConnectionError()
    mock_post_res = mock_post.return_value
    mock_post_res.status_code = 200
    mock_post_res.json.return_value = {
      "model": "gemma3:12b",
      "created_at": "2023-12-12T14:13:43.416799Z",
      "message": {
        "role": "assistant",
        "content": "Here is a recipe..."
      },
      "done": True,
      "total_duration": 5191566416,
      "load_duration": 2154458,
      "prompt_eval_count": 26,
      "prompt_eval_duration": 383809000,
      "eval_count": 298,
      "eval_duration": 4799921000
    }
    
    db_session.add(connection)
    db_session.add(model)
    db_session.commit()

    serv = LLMService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(DisabledModelError):
        serv.get_chat_completion(3, [
            SystemMessage("YOU ARE THE ONE NEO!"),
            UserMessage("Hello there!"),
            AssistantMessage("What can I help you with?"),
            UserMessage("Give me a recipe for fish and chips.")
        ])
