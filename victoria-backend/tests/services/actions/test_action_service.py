import pytest
import os
from unittest import mock
from app.services.action import ActionService, NonexistentActionError, NonexistentActionRepositoryError
from app.services.db import DatabaseService
from app.model.action_repository import ActionRepository
from app.model.action import Action
from app.model.invocation import Invocation
from requests import ConnectionError

from sqlalchemy import select

@pytest.fixture(scope="function")
def db_serv(db_factory, db_container):
    db = DatabaseService(db_url=db_container)
    
    with mock.patch.object(db, 'get_session_factory', return_value=db_factory):
        yield db

@mock.patch("tests.services.actions.test_action_service.ActionService.set_action_repository_actions")
@mock.patch("tests.services.actions.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_can_add_action_git_repository(mock_import_actions, mock_set_actions, db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    mock_import_actions.return_value = []
    
    # Act
    serv.add_action_repository("Home Assistant", "http://mygit.com/HATools")
    
    # Assert
    repos = db_session.scalars(
        select(ActionRepository)
    ).all()

    assert len(repos) == 1
    assert repos[0].name == "Home Assistant"
    assert repos[0].url == "http://mygit.com/HATools"
    assert repos[0].actions == []

@mock.patch("tests.services.actions.test_action_service.ActionService.set_action_repository_actions")
@mock.patch("tests.services.actions.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_tries_to_import_and_set_actions_for_added_repository(mock_import_actions, mock_set_actions, db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    think_action = Action(
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    mock_import_actions.return_value = [think_action, end_action]
    
    # Act
    serv.add_action_repository(name="Mandatory actions", url="ble")
    
    # Assert
    repo = db_session.scalar(
        select(ActionRepository)
    )

    assert repo is not None
    mock_import_actions.assert_called_once_with("ble")
    mock_set_actions.assert_called_once_with(repo.id, [think_action, end_action])

@mock.patch("tests.services.actions.test_action_service.ActionService.set_action_repository_actions")
@mock.patch("tests.services.actions.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_tries_to_reimport_and_set_actions_for_existing_repositories_when_constructed(mock_import_actions, mock_set_actions, db_serv, db_session):
    # Arrange
    repo_gitea = ActionRepository(
        id=600,
        name="Gitea",
        url="gitea"
    )
    repo_gitlab = ActionRepository(
        id=700,
        name="GitLab",
        url="gitlab"
    )
    db_session.add(repo_gitea)
    db_session.add(repo_gitlab)
    db_session.commit()

    think_action = Action(
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    mock_import_actions.side_effect = lambda url: {
        "gitea": [think_action],
        "gitlab": [end_action]
    }.get(url)
    
    # Act
    ActionService(
        database_service=db_serv
    )
    
    # Assert
    mock_import_actions.assert_any_call("gitea")
    mock_import_actions.assert_any_call("gitlab")

    mock_set_actions.assert_any_call(600, [think_action])
    mock_set_actions.assert_any_call(700, [end_action])

@mock.patch("tests.services.actions.test_action_service.ActionService.set_action_repository_actions")
@mock.patch("tests.services.actions.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_does_not_set_repository_actions_if_reimport_throws(mock_import_actions, mock_set_actions, db_serv, db_session):
    # Arrange
    think_action = Action(
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    repo_gitea = ActionRepository(
        id=600,
        name="Gitea",
        url="gitea",
        actions=[think_action, end_action]
    )
    db_session.add(repo_gitea)
    db_session.commit()
    mock_import_actions.side_effect = ConnectionError()
    
    # Act
    ActionService(
        database_service=db_serv
    )

    # Assert
    mock_import_actions.assert_called_once_with("gitea")
    mock_set_actions.assert_not_called()
    db_session.refresh(repo_gitea)
    assert repo_gitea.actions == [think_action, end_action]

def test_action_service_can_set_actions_for_action_repository(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    think_action = Action(
        id=1,
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        id=1337,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    repo_gitea = ActionRepository(
        id=600,
        name="Gitea",
        url="gitea",
        actions=[think_action, end_action]
    )
    db_session.add(repo_gitea)
    db_session.commit()
    
    # Act
    # FIXME: We should not rely solely on the function name to identify a function within a repository,
    # it should be the full module path to avoid collisions.
    new_action = Action(
        function_name="new",
        function_param_schema={
            "iterations": "int"
        },
        function_docstring="LOL",
        function_source_code=""
    )
    existing_action = Action(
        function_name="end_workflow",
        function_param_schema={
            "new_param": "int"
        },
        function_docstring="A new version of end_workflow",
        function_source_code=""
    )
    serv.set_action_repository_actions(600, [new_action, existing_action])
    
    # Arrange
    db_session.refresh(repo_gitea)
    assert len(repo_gitea.actions) == 2
    actions = db_session.scalars(
        select(Action)
        .order_by(Action.function_name)
    ).all()

    assert len(actions) == 2
    # This is an entirely new action, so it won't have the same id as an existing one
    assert actions[1].id != 1
    assert actions[1].function_name == "new"
    assert actions[1].function_param_schema == {
        "iterations": "int"
    }
    assert actions[1].function_docstring == "LOL"
    assert actions[1].function_source_code == ""

    # existing_action is not added as a new action, since it has the same function_name as end_action
    # so this is the same id as the id of end_action
    assert actions[0].id == 1337
    # New code and docstring
    assert actions[0].function_source_code == ""
    assert actions[0].function_docstring == "A new version of end_workflow"
    

@mock.patch("tests.services.actions.test_action_service.ActionService._clone_git_repository")
def test_action_service_imports_actions_from_simple_action_git_repository(mock_clone, db_serv, tmp_path):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    
    repo = tmp_path / "my_repo"
    mock_clone.return_value = str(repo)
    repo.mkdir()
    script = repo / "basic.py"
    script.touch()
    
    script.write_text(
"""
import requests

def tool(func)
    return func

# The tool decorator is just used as a marker, it does nothing
@tool
def my_cool_tool(idx: int, name_list: List[str]):
    return name_list[idx]
"""
    )
    
    # Act
    actions = serv.import_actions_from_git_url("https://github.com/PistaMista/victoria-default-actions")
    
    # Assert
    assert len(actions) == 1
    assert actions[0].function_name == "my_cool_tool"
    assert actions[0].function_param_schema == {
        "idx": "int",
        "name_list": "typing.List[str]"
    }
    # the rest is covered by test_tool_decorator

@mock.patch("tests.services.actions.test_action_service.ActionService._clone_git_repository")
def test_action_service_imports_actions_from_complex_action_git_repository(mock_clone, db_serv, tmp_path):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    
    repo = tmp_path / "my_repo"
    mock_clone.return_value = str(repo)
    repo.mkdir()
    
    calculator_tools = repo / "calculator"
    calculator_tools.mkdir()

    basic_math = calculator_tools / "basic_arithmetic.py"
    basic_math.touch()
    
    basic_math.write_text(
"""
import requests

def tool(func)
    return func

@tool
def add(a: int, b: int):
    return a + b

@tool
def sub(a: int, b: int):
    return a - b

@tool
def mul(a: int, b: int):
    return a * b
"""
    )
    
    complex_math = calculator_tools / "complex_arithmetic.py"
    complex_math.touch()
    
    complex_math.write_text(
"""
def tool(func):
    return func

@tool
def factorial(x: int):
    if x <= 0:
        return 1
    
    return x * factorial(x - 1)

@tool
def add_mod_3(a: int, b: int):
    return (a + b) % 3
"""
    )
    
    misc = repo / "misc.py"
    misc.touch()
    
    misc.write_text(
"""
def tool(func):
    return func

@tool
def quote(x: str):
    return '"' + x + '"'
"""
    )
    
    # Act
    actions = serv.import_actions_from_git_url("https://github.com/PistaMista/victoria-default-actions")
    
    # Assert
    func_names = list(map(lambda x: x.function_name, actions))

    assert "add" in func_names
    assert "sub" in func_names
    assert "mul" in func_names
    assert "factorial" in func_names
    assert "add_mod_3" in func_names
    assert "quote" in func_names
    

@mock.patch("tests.services.actions.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_can_remove_action_git_repository(mock_import_actions, db_serv, db_session):
    # Arrange
    repo = ActionRepository(
        id=42,
        name="Gitea",
        url="gitea",
        actions=[]
    )
    db_session.add(repo)
    db_session.commit()

    mock_import_actions.side_effect = ConnectionError() # So that ActionService does not try to reimport the actions
    serv = ActionService(
        database_service=db_serv
    )
    
    # Act
    serv.remove_action_repository(42)

    # Assert
    repos = db_session.scalars(
        select(ActionRepository)
    )
    assert repos.first() is None

@mock.patch("tests.services.actions.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_deletes_actions_imported_from_removed_git_repository(mock_import_actions, db_serv, db_session):
    # Arrange
    think_action = Action(
        function_name="think",
        function_param_schema={},
        function_docstring="Some docs idk",
        function_source_code=""
    )
    end_action = Action(
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool"
        },
        function_docstring="Some docs idk",
        function_source_code=""
    )
    repo = ActionRepository(
        id=42,
        name="Gitea",
        url="gitea",
        actions=[think_action, end_action]
    )
    db_session.add(repo)
    db_session.commit()

    mock_import_actions.side_effect = ConnectionError() # So that ActionService does not try to reimport the actions
    serv = ActionService(
        database_service=db_serv
    )
    
    # Act
    serv.remove_action_repository(42)

    # Assert
    actions = db_session.scalars(
        select(Action)
    )
    assert actions.first() is None

def test_action_service_can_get_action_descriptions(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )

    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[think_action, end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    desc1 = serv.get_action_description(10)
    desc2 = serv.get_action_description(20)
    
    assert desc1 == \
"""{
    "action_name": "think",
    "description": "Returns its parameter. Use to append a thought verbatim to the workflow.",
    "parameters": {
        "content": str
    }
}"""
    assert desc2 == \
"""{
    "action_name": "end_workflow",
    "description": "Ends the workflow either with success or failure for the given reason.",
    "parameters": {
        "successful": bool,
        "reason": str
    }
}"""

def test_action_service_parses_valid_invocation_json(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )

    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[think_action, end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    res = serv.parse_invocation("""
    {
        "action_name": "end_workflow",
        "arguments": {
            "successful": true,
            "reason": "Replied to user greeting."
        }
    }
    """)

    assert res.action == end_action
    assert res.function_name == "end_workflow"
    assert res.params == {
        "successful": True,
        "reason": "Replied to user greeting."
    }
    assert res.function_name_semantically_valid
    assert res.params_semantically_valid

def test_action_service_parses_valid_invocation_json_with_any_leading_or_trailing_text(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )

    think_action = Action(
        id=10,
        function_name="think",
        function_param_schema={
            "content": "str"
        },
        function_docstring="Returns its parameter. Use to append a thought verbatim to the workflow.",
        function_source_code=""
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[think_action, end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    res = serv.parse_invocation("""
    I can include code blocks and other kinds of leading garbage characters here!

    ```json
    {
        "action_name": "end_workflow",
        "arguments": {
            "successful": true,
            "reason": "Replied to user greeting."
        }
    }
    ```
    """)

    assert res.action == end_action
    assert res.function_name == "end_workflow"
    assert res.params == {
        "successful": True,
        "reason": "Replied to user greeting."
    }
    assert res.function_name_semantically_valid
    assert res.params_semantically_valid

def test_action_service_parses_syntactically_invalid_invocation_json(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    res = serv.parse_invocation("""
    {
        "action_name": "end_workflow",
        "arguments": {
            "successful": true,
            "reason": "Replied to user greeting."
        \}
    }
    """)

    assert isinstance(res, Invocation)
    assert res.action is None
    assert res.function_name is None
    assert res.params is None
    assert not res.function_name_semantically_valid
    assert not res.params_semantically_valid

def test_action_service_parses_semantically_invalid_invocation_json_with_incorrect_function_name(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    res = serv.parse_invocation("""
    {
        "action_name": "stop_workflow",
        "arguments": {
            "successful": true,
            "reason": "Replied to user greeting."
        }
    }
    """)

    assert isinstance(res, Invocation)
    assert res.action is None
    assert res.function_name == "stop_workflow"
    assert res.params == {
        "successful": True,
        "reason": "Replied to user greeting."
    }
    assert not res.function_name_semantically_valid
    assert not res.params_semantically_valid

def test_action_service_parses_semantically_invalid_invocation_json_with_missing_arguments(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    res = serv.parse_invocation("""
    {
        "action_name": "end_workflow",
        "arguments": {
            "successful": true
        }
    }
    """)

    assert isinstance(res, Invocation)
    assert res.action == end_action
    assert res.function_name == "end_workflow"
    assert res.params == {
        "successful": True
    }
    assert res.function_name_semantically_valid
    assert not res.params_semantically_valid

def test_action_service_parses_semantically_invalid_invocation_json_with_extraneous_arguments(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    res = serv.parse_invocation("""
    {
        "action_name": "end_workflow",
        "arguments": {
            "successful": true,
            "reason": "Reason!",
            "id": 40
        }
    }
    """)

    assert isinstance(res, Invocation)
    assert res.action == end_action
    assert res.function_name == "end_workflow"
    assert res.params == {
        "successful": True,
        "reason": "Reason!",
        "id": 40
    }
    assert res.function_name_semantically_valid
    assert not res.params_semantically_valid

def test_action_service_parses_semantically_invalid_invocation_json_with_invalid_argument_types(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    end_action = Action(
        id=20,
        function_name="end_workflow",
        function_param_schema={
            "successful": "bool",
            "reason": "str"
        },
        function_docstring="Ends the workflow either with success or failure for the given reason.",
        function_source_code=""
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[end_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    # Act
    res = serv.parse_invocation("""
    {
        "action_name": "end_workflow",
        "arguments": {
            "successful": true,
            "reason": 3.14
        }
    }
    """)

    assert isinstance(res, Invocation)
    assert res.action == end_action
    assert res.function_name == "end_workflow"
    assert res.params == {
        "successful": True,
        "reason": 3.14
    }
    assert res.function_name_semantically_valid
    assert not res.params_semantically_valid

def test_action_service_executes_valid_invocation_with_function_result_as_string(db_serv, db_session):
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    factorial_action = Action(
        id=20,
        function_name="factorial",
        function_param_schema={
            "x": "int"
        },
        function_docstring="Calculates the factorial of the given number",
        function_source_code="""
@tool
def factorial(x: int):
    if x <= 0:
        return 1
    
    return x * factorial(x - 1)
        """
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[factorial_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    invocation = Invocation(
        action=factorial_action,
        function_name="factorial",
        params={
            "x": 4
        },
        function_name_semantically_valid=True,
        params_semantically_valid=True
    )
    
    # Act
    res = serv.execute_invocation(invocation)
    assert res == "24"
    
def test_action_service_executes_invalid_invocation_with_error_result_as_string():
    # Arrange
    serv = ActionService(
        database_service=db_serv
    )
    factorial_action = Action(
        id=20,
        function_name="factorial",
        function_param_schema={
            "x": "int"
        },
        function_docstring="Calculates the factorial of the given number",
        function_source_code="""
@tool
def factorial(x: int):
    if x <= 0:
        return 1
    
    return x * factorial(x - 1)
        """
    )
    repo = ActionRepository(
        name="Gitea",
        url="gitea",
        actions=[factorial_action]
    )
    db_session.add(repo)
    db_session.commit()
    
    inv_failed_name_parse = Invocation(
        action=None,
        function_name=None,
        params={
            "x": 4
        },
        function_name_semantically_valid=False,
        params_semantically_valid=False
    )
    inv_failed_arg_parse = Invocation(
        action=factorial_action,
        function_name="factorial",
        params=None,
        function_name_semantically_valid=True,
        params_semantically_valid=False
    )
    inv_func_wrong = Invocation(
        action=None,
        function_name="factorialeeeee",
        params={
            "x": 4
        },
        function_name_semantically_valid=False,
        params_semantically_valid=False
    )
    inv_param_wrong = Invocation(
        action=factorial_action,
        function_name="factorial",
        params={
            "y": 4
        },
        function_name_semantically_valid=True,
        params_semantically_valid=False
    )
    
    # Act
    res_failed_name_parse = serv.execute_invocation(inv_failed_name_parse)
    res_failed_arg_parse = serv.execute_invocation(inv_failed_arg_parse)
    res_func_wrong = serv.execute_invocation(inv_func_wrong)
    res_param_wrong = serv.execute_invocation(inv_param_wrong)
    
    # Assert
    assert isinstance(res_failed_name_parse, str)
    assert isinstance(res_failed_arg_parse, str)
    assert isinstance(res_func_wrong, str)
    assert isinstance(res_param_wrong, str)


def test_action_service_throws_when_trying_to_manipulate_nonexistent_repo(db_serv, db_session):
    # Arrange
    repo = ActionRepository(
        id=42,
        name="Gitea",
        url="gitea",
        actions=[]
    )
    db_session.add(repo)
    db_session.commit()

    mock_import_actions.side_effect = ConnectionError() # So that ActionService does not try to reimport the actions
    serv = ActionService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(NonexistentActionRepositoryError):
        serv.remove_action_repository(43)

    with pytest.raises(NonexistentActionRepositoryError):
        serv.set_action_repository_actions(43, [])


def test_action_service_throws_when_trying_to_manipulate_nonexistent_action(db_serv, db_session):
    # Arrange
    repo = ActionRepository(
        id=42,
        name="Gitea",
        url="gitea",
        actions=[]
    )
    db_session.add(repo)
    db_session.commit()

    mock_import_actions.side_effect = ConnectionError() # So that ActionService does not try to reimport the actions
    serv = ActionService(
        database_service=db_serv
    )
    
    # Act / Assert
    with pytest.raises(NonexistentActionError):
        serv.get_action_description(1)