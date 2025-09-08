import pytest
from unittest import mock

@mock.patch("tests.action.test_action_service.ActionService.set_action_repository_actions")
@mock.patch("tests.action.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_can_add_action_git_repository(mock_import):
    assert False

@mock.patch("tests.action.test_action_service.ActionService.set_action_repository_actions")
@mock.patch("tests.action.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_tries_to_import_actions_for_added_repository(mock_import):
    assert False

@mock.patch("tests.action.test_action_service.ActionService.set_action_repository_actions")
@mock.patch("tests.action.test_action_service.ActionService.import_actions_from_git_url")
def test_action_service_tries_to_import_actions_for_existing_repositories_when_constructed(mock_import):
    assert False

def test_action_service_imports_actions_from_simple_action_git_repository():
    assert False

def test_action_service_imports_actions_from_complex_action_git_repository():
    assert False

def test_action_service_can_remove_action_git_repository():
    assert False

def test_action_service_deletes_actions_imported_from_removed_git_repository():
    assert False

def test_action_service_can_get_action_description():
    assert False

def test_action_service_parses_valid_invocation_json():
    assert False

def test_action_service_parses_valid_invocation_json_with_any_leading_or_trailing_text():
    assert False

def test_action_service_parses_syntactically_invalid_invocation_json():
    assert False

def test_action_service_parses_semantically_invalid_invocation_json_with_incorrect_function_name():
    assert False

def test_action_service_parses_semantically_invalid_invocation_json_with_missing_arguments():
    assert False

def test_action_service_parses_semantically_invalid_invocation_json_with_extraneous_arguments():
    assert False

def test_action_service_parses_semantically_invalid_invocation_json_with_invalid_argument_types():
    assert False

def test_action_service_executes_valid_invocation_with_function_result_as_string():
    assert False
    
def test_action_service_executes_invalid_invocation_with_error_result_as_string():
    assert False

def test_action_service_throws_when_trying_to_manipulate_nonexistent_repo():
    assert False