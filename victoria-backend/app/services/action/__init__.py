from app.services.db import DatabaseService
from app.model.action import Action
from app.model.invocation import Invocation
from app.model.action_repository import ActionRepository
from sqlalchemy import select
from typing import List

TOOL_REGISTRY = []

class ActionService:
    
    def __init__(
        self,
        database_service: DatabaseService
    ):
        self._db: DatabaseService = database_service
        self._reimport_actions_for_existing_repositories()


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
        
        try:
            actions = self.import_actions_from_git_url(url)
            self.set_action_repository_actions(repo_id, actions)
        except:
            # TODO: Store an error somewhere indicating that the last import action failed
            pass
    
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

    def _reimport_actions_for_existing_repositories(self):
        repos = []
        with self._db.session() as db:
            repos = db.scalars(
                select(ActionRepository)
            ).all()
        
        for repo in repos:
            try:
                actions = self.import_actions_from_git_url(repo.url)
                self.set_action_repository_actions(repo.id, actions)
            except:
                # TODO: Store an error somewhere indicating that the import failed
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
    