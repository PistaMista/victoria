from app.services.db import DatabaseService
from app.model.llm_connection import OllamaConnection, LLMConnection
from app.model.language_model import LanguageModel
from sqlalchemy import select
import requests
from typing import List

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

    
    def add_ollama_connection(self, name: str, url: str):
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
        pass
    
    def _get_ollama_chat_completion(self, model_id: int, messages: List["Message"]) -> "AssistantMessage":
        pass

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

class SystemMessage(Message):
    pass

class AssistantMessage(Message):
    pass

class UserMessage(Message):
    pass

class NonexistentConnectionError(Exception):
    def __init__(self, id: int):
        super().__init__(f"the connection with id {id} does not exist")

class NonexistentModelError(Exception):
    def __init__(self, id: int):
        super().__init__(f"the model with id {id} does not exist")

class DisabledModelError(Exception):
    def __init__(self, id: int):
        super().__init__(f"the model with id {id} is disabled and cannot be used")

class OllamaCommunicationError(Exception):
    def __init__(self):
        super().__init__("failed to communicate with Ollama server")