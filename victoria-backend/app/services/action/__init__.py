from app.services.db import DatabaseService
from app.services.action.tool import convert_to_action
from app.model.user import User
from app.model.action import Action
from app.model.invocation import Invocation
from app.model.action_repository import ActionRepository
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import List, Optional, Dict, Any
from git import Repo
from pydantic import TypeAdapter, ValidationError, BaseModel
from pydoc import locate
import requests
import re
import json
import tempfile
import shutil
import os
import ast
import typing


class ActionService:
    def __init__(self, database_service: DatabaseService):
        self._db: DatabaseService = database_service
        self._reimport_actions_for_existing_repositories()

    def get_all_action_repositories(self) -> List[ActionRepository]:
        """Returns all registered action repositories."""
        with self._db.session() as db:
            res = (
                db.scalars(
                    select(ActionRepository).options(
                        joinedload(ActionRepository.actions)
                    )
                )
                .unique()
                .all()
            )

            return res

    def get_action_repository_by_id(self, id: int) -> ActionRepository:
        """Gets the action repository with the given id."""
        with self._db.session() as db:
            res = db.scalar(
                select(ActionRepository)
                .where(ActionRepository.id == id)
                .options(joinedload(ActionRepository.actions))
            )

            if res is None:
                raise NonexistentActionRepositoryError(id)

            return res

    def update_action_repository(self, id: int, changes: "ActionRepositoryDiff"):
        """Updates the action repository with the given id."""
        with self._db.session() as db:
            repo = db.scalar(
                select(ActionRepository)
                .where(ActionRepository.id == id)
                .with_for_update()
            )

            if repo is None:
                raise NonexistentActionRepositoryError(id)

            if changes.name is not None:
                repo.name = changes.name

            if changes.url is not None:
                repo.url = changes.url

            db.commit()

        self._reimport_actions_for_existing_repositories()

    def get_user_permitted_actions(self, user_id: int) -> List[Action]:
        """Gets the actions that agents of the user with the given id can take."""
        with self._db.session() as db:
            res = (
                db.scalars(
                    select(Action)
                    .join(Action.allowed_on_users)
                    .where(User.id == user_id)
                    .order_by(Action.function_name)
                ).all()
                or []
            )

            return res

    def get_all_actions(self) -> List[Action]:
        """Gets all the currently registered actions."""
        with self._db.session() as db:
            res = db.scalars(select(Action).order_by(Action.function_name)).all() or []

            return res

    def add_action_repository(self, name: str, url: str) -> int:
        """Adds an action repository with the given name and url."""
        repo_id = 0
        with self._db.session() as db:
            repo = ActionRepository(name=name, url=url)

            db.add(repo)
            db.commit()
            db.refresh(repo)

            repo_id = repo.id

        try:
            print(f"Importing actions from {url}...")
            actions = self.import_actions_from_git_url(url)
            self.set_action_repository_actions(repo_id, actions)
        except Exception as e:
            print(e)
            # TODO: Store an error somewhere indicating that the last import action failed
            pass

        return repo_id

    def remove_action_repository(self, id: int):
        with self._db.session() as db:
            repo = db.scalar(
                select(ActionRepository)
                .where(ActionRepository.id == id)
                .with_for_update()
            )

            if repo is None:
                raise NonexistentActionRepositoryError(id)

            db.delete(repo)
            db.commit()

    def import_actions_from_git_url(self, url: str) -> List[Action]:
        repo_files = self._clone_git_repository(url)
        actions = self._import_actions_from_local_directory(repo_files)
        shutil.rmtree(repo_files)
        return actions

    def set_action_repository_actions(self, repo_id: int, actions: List[Action]):
        # FIXME: We should not rely solely on the function name to identify a function within a repository,
        # it should be the full module path to avoid name collisions.
        with self._db.session() as db:
            repo = db.scalar(
                select(ActionRepository)
                .where(ActionRepository.id == repo_id)
                .with_for_update()
            )

            if repo is None:
                raise NonexistentActionRepositoryError(repo_id)

            repo_actions = db.scalars(
                select(Action).where(Action.repository_id == repo.id).with_for_update()
            )

            for existing in repo_actions:
                for i, new in enumerate(actions):
                    if new.function_name == existing.function_name:
                        actions.pop(i)

                        existing.function_param_schema = new.function_param_schema
                        existing.function_docstring = new.function_docstring
                        existing.function_source_code = new.function_source_code
                        break
                else:
                    db.delete(existing)

            for new in actions:
                repo.actions.append(new)

            db.commit()

    def parse_invocation(self, invocation_text: str) -> Invocation:
        result = Invocation(
            action=None,
            function_name=None,
            params=None,
            function_name_semantically_valid=False,
            params_semantically_valid=False,
        )

        # Parse JSON
        try:
            trimmed = re.match(r"[^{]*({[\s\S]*})[^}]*", invocation_text).group(1)
            parsed = json.loads(trimmed)

            result.function_name = parsed.get("action_name", None)
            result.params = parsed.get("arguments", None)
        except Exception:
            pass

        # Retrieve action with same name
        # FIXME: This is a vulnerability! Multiple users may have an action with the same
        # name, but the one which is first in the database will always be used!
        # The function_name is not unique!
        # Maybe use action IDs instead?
        if result.function_name is not None:
            with self._db.session() as db:
                action = db.scalar(
                    select(Action).where(Action.function_name == result.function_name)
                )

                if action is not None:
                    result.action = action
                    result.function_name_semantically_valid = True

        if result.action is not None and isinstance(result.params, dict):
            # Validate params
            args = result.params.items()
            params = result.action.function_param_schema.items()

            if len(args) == len(params):
                for (arg_name, arg_val), (param_name, param_type) in zip(args, params):
                    if arg_name != param_name:
                        break

                    type_class = locate(param_type)
                    if type_class is None:
                        break

                    try:
                        type_adapter = TypeAdapter(type_class)
                        type_adapter.validate_python(arg_val)
                    except ValidationError:
                        break
                else:
                    result.params_semantically_valid = True

        return result

    def execute_invocation(
        self, invocation: Invocation, context: Dict[str, Any]
    ) -> str:
        errors = []

        if invocation.function_name is not None:
            if not invocation.function_name_semantically_valid:
                errors.append(
                    "The action name you provided does not refer to a valid action. Please check the list of valid actions."
                )
        else:
            errors.append(
                "Could not parse action name out of your JSON response, please check the format."
            )

        if invocation.params is not None:
            if not invocation.params_semantically_valid:
                errors.append(
                    "The arguments you provided are not semantically valid. Please check their names and types."
                )
        else:
            errors.append(
                "Could not parse action arguments out of your JSON response, please check the format."
            )

        if errors:
            errors_str = "\n".join(errors)
            return f"Errors:\n{errors_str}"

        try:
            namespace = {"tool": lambda x: x, "requests": requests}
            exec(invocation.action.function_source_code, namespace)
            return str(
                namespace[invocation.action.function_name](
                    context=context, **invocation.params
                )
            )
        except Exception as e:
            return str(e)

    def get_action_description(self, action_id: int) -> str:
        with self._db.session() as db:
            action = db.scalar(select(Action).where(Action.id == action_id))

            if action is None:
                raise NonexistentActionError(action_id)

            # This is not supposed to be strictly valid JSON,
            # just something easier to parse for the LLM.
            desc = "{\n"
            desc += f'    "action_name": "{action.function_name}",\n'
            desc += f'    "description": "{action.function_docstring}",\n'
            desc += '    "parameters": {\n'
            for name, typ in action.function_param_schema.items():
                desc += f'        "{name}": {typ},\n'
            desc += "    }\n"
            desc += "}"

            return desc

    def _reimport_actions_for_existing_repositories(self):
        repos = []
        with self._db.session() as db:
            repos = db.scalars(select(ActionRepository)).all()

        for repo in repos:
            try:
                actions = self.import_actions_from_git_url(repo.url)
                self.set_action_repository_actions(repo.id, actions)
            except Exception:
                # TODO: Store an error somewhere indicating that the import failed
                pass

    def _import_actions_from_local_directory(self, path: str) -> List[Action]:
        actions = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(".py"):
                    py_path = os.path.join(dirpath, filename)
                    actions.extend(self._import_actions_from_python_file(py_path))

        return actions

    def _import_actions_from_python_file(self, path: str):
        actions = []
        source = ""

        with open(path, "r") as f:
            source = f.read()

        module = ast.parse(source)
        tool_defs = [
            x
            for x in module.body
            if isinstance(x, ast.FunctionDef)
            and any(d.id == "tool" for d in x.decorator_list)
        ]

        for tool_def in tool_defs:
            namespace = {
                "tool": lambda x: x,
                "typing": typing,
            }
            namespace.update(vars(typing))

            tool_module = ast.Module(body=[tool_def])

            exec(compile(source=tool_module, filename=path, mode="exec"), namespace)
            func = namespace[tool_def.name]
            action = convert_to_action(func)
            actions.append(action)

        return actions

    def _clone_git_repository(self, url: str) -> str:
        """Clones the given Git repository and returns the path to the clone directory."""
        temp_dir = tempfile.mkdtemp("victoria-action-import")
        Repo.clone_from(url, temp_dir)
        return temp_dir


class ActionRepositoryDiff(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None


class NonexistentActionRepositoryError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent action repository: {id}")


class NonexistentActionError(Exception):
    def __init__(self, id: int):
        super().__init__(f"nonexistent action: {id}")
