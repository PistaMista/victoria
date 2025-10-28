from app.services.db import DatabaseService
from app.model.llm_connection import OllamaConnection, LLMConnection
from app.model.language_model import LanguageModel
from sqlalchemy import select
from pydantic import BaseModel
import requests
from typing import List, Optional

class LLMService:
    def __init__(
        self,
        database_service: DatabaseService
    ):
        self._db: DatabaseService = database_service
        
        with self._db.session() as db:
            connections = db.scalars(
                select(OllamaConnection)
            )
            
            for conn in connections:
                try:
                    self._refresh_ollama_connection_models(conn.id)
                except OllamaCommunicationError:
                    # TODO: Log the connection failure?
                    pass

    def get_enabled_models(self) -> List[LanguageModel]:
        """Gets all currently enabled LanguageModels."""
        with self._db.session() as db:
            res = db.scalars(
                select(LanguageModel).where(LanguageModel.enabled)
            ).all()

            return res

    def get_all_models(self) -> List[LanguageModel]:
        """Gets all available LanguageModels."""
        with self._db.session() as db:
            res = db.scalars(select(LanguageModel)).all()
            return res

    def set_model_enabled_by_id(self, model_id: int, enabled: bool):
        """Enables or disables the given LanguageModel."""
        with self._db.session() as db:
            model = db.scalar(
                select(LanguageModel).where(LanguageModel.id == model_id)
            )

            if model is None:
                raise NonexistentModelError(model_id)

            model.enabled = enabled
            db.commit()

    def get_all_connections(self) -> List[LLMConnection]:
        """Gets all registered connections."""
        pass

    def get_connection_by_id(self, id: int) -> LLMConnection:
        """Gets the connection with the given ID."""
        pass

    def update_ollama_connection(self, id: int, changes: "OllamaConnectionDiff"):
        """Updates the given Connection's settings."""
        pass
    
    def add_ollama_connection(self, name: str, url: str) -> int:
        with self._db.session() as db:
            connection = OllamaConnection(
                name=name,
                url=url,
                models=self._import_ollama_models(url)
            )
            
            db.add(connection)
            db.commit()
    
    def remove_connection(self, id: int):
        with self._db.session() as db:
            connection = db.scalar(
                select(LLMConnection).where(LLMConnection.id == id)
            )
            
            if connection is None:
                raise NonexistentConnectionError(id)
            
            db.delete(connection)
            db.commit()

    def get_chat_completion(self, model_id: int, messages: List["Message"]) -> "AssistantMessage":
        with self._db.session() as db:
            model = db.scalar(
                select(LanguageModel).where(LanguageModel.id == model_id)
            )
            
            if model is None:
                raise NonexistentModelError(model_id)
            
            if not model.enabled:
                raise DisabledModelError(model_id)

            connection = model.connection
            
            if isinstance(connection, OllamaConnection):
                return self._get_ollama_chat_completion(model.name, connection.url, messages)
            else:
                raise UnrecognizedConnectionTypeError(connection.id)
            
    
    def _get_ollama_chat_completion(self, model_name: str, url: str, messages: List["Message"]) -> "AssistantMessage":
        try:
            res = requests.post(f"{url}/api/chat", json={
                "model": model_name,
                "stream": False,
                "messages": [msg.to_json() for msg in messages]
            })
            json = res.json()

            return AssistantMessage(json["message"]["content"])
        except (requests.RequestException, requests.HTTPError):
            raise OllamaCommunicationError()

    def _refresh_ollama_connection_models(self, id: int):
        with self._db.session() as db:
            connection = db.scalar(
                select(OllamaConnection)
                .where(OllamaConnection.id == id)
            )
            
            if connection is None:
                raise NonexistentConnectionError(id)

            current_models = self._import_ollama_models(connection.url)
            
            # Delete models that no longer exist on the remote
            for model in connection.models:
                if not any(m.name == model.name for m in current_models):
                    db.delete(model)

            # Add models that are new on the remote
            for model in current_models:
                if not any(m.name == model.name for m in connection.models):
                    connection.models.append(model)
            
            db.commit()

    def _import_ollama_models(self, ollama_url: str) -> List[LanguageModel]:
        try:
            models = []

            res = requests.get(f"{ollama_url}/api/tags")
            res.raise_for_status()
            json = res.json()
            
            for model_dict in json["models"]:
                model = LanguageModel(
                    name=model_dict["name"],
                    enabled=True
                )
                
                models.append(model)
            
            return models
        except (requests.RequestException, requests.HTTPError):
            raise OllamaCommunicationError()

    
    

class Message:
    def __init__(self, content: str):
        self._content: str = content
    
    def __eq__(self, o: object) -> bool:
        return type(self) is type(o) and self._content == o._content
    
    def to_json(self) -> dict:
        return {
            "role": "unknown",
            "content": self._content
        }

class SystemMessage(Message):
    def to_json(self) -> dict:
        res = super().to_json()
        res["role"] = "system"
        return res

class AssistantMessage(Message):
    def to_json(self) -> dict:
        res = super().to_json()
        res["role"] = "assistant"
        return res

class UserMessage(Message):
    def to_json(self) -> dict:
        res = super().to_json()
        res["role"] = "user"
        return res

class OllamaConnectionDiff(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None

class NonexistentConnectionError(Exception):
    def __init__(self, id: int):
        super().__init__(f"the connection with id {id} does not exist")

class UnrecognizedConnectionTypeError(Exception):
    def __init__(self, id: int):
        super().__init__(f"the connection with id {id} has an unsupported type")

class NonexistentModelError(Exception):
    def __init__(self, id: int):
        super().__init__(f"the model with id {id} does not exist")

class DisabledModelError(Exception):
    def __init__(self, id: int):
        super().__init__(f"the model with id {id} is disabled and cannot be used")

class OllamaCommunicationError(Exception):
    def __init__(self):
        super().__init__("failed to communicate with Ollama server")
