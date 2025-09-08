from app.services.db import DatabaseService
from app.model.action import Action
from app.model.invocation import Invocation
from app.model.action_repository import ActionRepository
from typing import List

TOOL_REGISTRY = []

class ActionService:
    
    def __init__(
        self,
        database_service: DatabaseService
    ):
        self._db: DatabaseService = database_service


    def add_action_repository(self, name: str, url: str):
        """Adds an action repository with the given name and url."""
        repo_id = 0
        with self._db.session() as db:
            repo = ActionRepository(
                name=name,
                url=url
            )
            
            db.add(repo)
            db.commit()
            db.refresh(repo)
            
            repo_id = repo.id
        
        actions = self.import_actions_from_git_url(url)
        self.set_action_repository_actions(repo_id, actions)
    
    def remove_action_repository(self, id: int):
        pass

    def import_actions_from_git_url(self, url: str) -> List[Action]:
        pass
    
    def set_action_repository_actions(self, repo_id: int, actions: List[Action]):
        pass

    def parse_invocation(self, invocation_text: str) -> Invocation:
        pass
    
    def execute_invocation(self, invocation: Invocation) -> str:
        pass

    def get_action_description(self, action_id: int) -> str:
        pass

    def _import_actions_from_local_directory(self, path: str) -> List[Action]:
        pass

    def _clone_git_repository(self, url: str) -> str:
        """Clones the given Git repository and returns the path to the clone directory."""
        pass

class NonexistentActionRepositoryError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent action repository: {id}")

class NonexistentActionError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent action: {id}")
    