import pytest
from app.services.monologues import NonexistentMonologueError
from app.services.monologues.runner.monologue_thread import AgenticMonologueThread
from app.services.llm import Message, SystemMessage, UserMessage, AssistantMessage
from app.model.thought import Thought
from app.model.invocation import Invocation
from app.model.monologue import Monologue, MonologueStatus
from app.model.agent import Agent
from app.model.action import Action
from app.model.trigger import Trigger
from unittest import mock
from datetime import datetime, UTC

# The agentic thread needs to:
# 1. (MonologueService) Convert the thoughts, agent prompt and tool descriptions to a sequence of System/User/Assistant messages
# 2. (LLMService) Call the LLM service with the appropriate model id and the converted chat
# 3. (ActionService) Parse the resulting AssistantMessage as an Invocation
# 4. (ActionService) Call the appropriate action
# 5. Combine the parsed call parameters and the result of the action into a Thought
# 6. (MonologueService) Append the thought to the monologue
# 7. Repeat


@pytest.fixture(scope="function")
def mock_monologue_serv():
    serv = mock.MagicMock()
    chat_history = [
        UserMessage("An email has arrived"),
        AssistantMessage('{"action_name": "think", "arguments": {"content": "Lol"}}'),
    ]
    serv.get_monologue_by_id.return_value = Monologue(
        id=1,
        title="None",
        summary="None",
        # event=event,
        agent=Agent(name="Cook", model_id=5),
        # lets say the server crashed while the monologue was running
        status=MonologueStatus.RUNNING,
        thoughts=[],
    )
    serv.get_monologue_thoughts_as_llm_chat_history.return_value = chat_history
    serv.get_monologue_system_prompt.return_value = "MY SYSTEM PROMPT"
    return serv


@pytest.fixture(scope="function")
def mock_llm_serv():
    serv = mock.MagicMock()
    msg_content = """
    {
        "action_name": "think",
        "arguments": {
            "content": "Lol"
        }
    }
    """
    serv.get_chat_completion.return_value = AssistantMessage(msg_content)
    return serv


@pytest.fixture(scope="function")
def mock_action_serv():
    serv = mock.MagicMock()
    invocation = Invocation(
        action=None, function_name="think", params={"content": "hello"}
    )
    serv.parse_invocation.return_value = invocation
    serv.execute_invocation.return_value = "hello"
    return serv


@pytest.fixture(scope="function")
def mock_on_finish():
    return mock.MagicMock()


@pytest.fixture(scope="function")
def thread_sut(mock_monologue_serv, mock_llm_serv, mock_action_serv, mock_on_finish):
    return AgenticMonologueThread(
        monologue_id=1,
        on_finish=mock_on_finish,
        monologue_service=mock_monologue_serv,
        llm_service=mock_llm_serv,
        action_service=mock_action_serv,
    )


def test_agentic_thread_calls_monologue_service_properly_on_iteration(
    thread_sut, mock_monologue_serv, mock_llm_serv
):
    # Act
    thread_sut.do_iteration()

    # Assert
    mock_monologue_serv.get_monologue_thoughts_as_llm_chat_history.assert_called_once_with(
        1
    )
    mock_monologue_serv.get_monologue_system_prompt.assert_called_once_with(1)
    mock_monologue_serv.get_monologue_by_id.assert_called_once_with(1)


def test_agentic_thread_calls_llm_service_properly_on_iteration(
    thread_sut, mock_monologue_serv, mock_llm_serv
):
    # Act
    thread_sut.do_iteration()

    # Assert
    # ...LLM service is called with the agent ID and the chat history
    mock_llm_serv.get_chat_completion.assert_called_once_with(
        5,
        [
            SystemMessage("MY SYSTEM PROMPT"),
            UserMessage("An email has arrived"),
            AssistantMessage(
                '{"action_name": "think", "arguments": {"content": "Lol"}}'
            ),
        ],
    )


def test_agentic_thread_calls_action_service_to_convert_llm_message_to_invocation_on_iteration(
    thread_sut, mock_llm_serv, mock_action_serv
):
    # Act
    thread_sut.do_iteration()

    # Assert
    mock_action_serv.parse_invocation.assert_called_once_with(
        mock_llm_serv.get_chat_completion.return_value._content
    )


def test_agentic_thread_calls_execute_invocation_with_fresh_context_when_no_context_set_on_iteration(
    thread_sut, mock_action_serv, mock_monologue_serv
):
    # Arrange
    mock_monologue_serv.get_monologue_by_id.return_value.context = None

    # Act
    thread_sut.do_iteration()

    # Assert
    mock_action_serv.execute_invocation.assert_called_once_with(
        mock_action_serv.parse_invocation.return_value, {}
    )


def test_agentic_thread_calls_execute_invocation_with_existing_context_when_context_set_on_iteration(
    thread_sut, mock_action_serv, mock_monologue_serv
):
    # Arrange
    mock_monologue_serv.get_monologue_by_id.return_value.context = {
        "BASE_URL": "MEGAURL",
        "TOKEN": 420,
    }

    # Act
    thread_sut.do_iteration()

    # Assert
    mock_action_serv.execute_invocation.assert_called_once_with(
        mock_action_serv.parse_invocation.return_value,
        {"BASE_URL": "MEGAURL", "TOKEN": 420},
    )


@mock.patch("app.services.monologues.runner.monologue_thread.datetime")
def test_agentic_thread_appends_new_thought_to_monologue_on_iteration(
    mock_datetime, thread_sut, mock_monologue_serv, mock_action_serv
):
    # Arrange
    mock_datetime.now.return_value = datetime.fromtimestamp(5001, tz=UTC)

    # Act
    thread_sut.do_iteration()

    # Assert
    mock_monologue_serv.append_thought_to_monologue.assert_called_once()
    arg = mock_monologue_serv.append_thought_to_monologue.call_args[0][1]

    assert arg.invocation.function_name == "think"
    assert arg.invocation.params["content"] == "hello"
    assert arg.result == "hello"
    assert arg.timestamp == datetime.fromtimestamp(5001, tz=UTC)


def test_agentic_thread_sets_monologue_context_on_iteration(
    thread_sut, mock_monologue_serv, mock_action_serv
):
    # Arrange
    mock_monologue_serv.get_monologue_by_id.return_value.context = {
        "BASE_URL": "MEGAURL",
        "TOKEN": 420,
    }

    def mock_exec(_, context):
        context["Woo"] = True
        return ""

    mock_action_serv.execute_invocation.side_effect = mock_exec

    # Act
    thread_sut.do_iteration()

    # Assert
    mock_monologue_serv.set_monologue_context.assert_called_once_with(
        1, {"BASE_URL": "MEGAURL", "TOKEN": 420, "Woo": True}
    )


def test_agentic_thread_stops_when_monologue_is_marked_as_succeeded(
    thread_sut, mock_monologue_serv, mock_on_finish
):
    # Act
    thread_sut.start()
    mock_monologue_serv.get_monologue_by_id.return_value.status = (
        MonologueStatus.SUCCESS
    )

    thread_sut.join()

    # Assert
    mock_on_finish.assert_called_once_with(thread_sut)


def test_agentic_thread_stops_when_monologue_is_marked_as_failed(
    thread_sut, mock_monologue_serv, mock_on_finish
):
    # Act
    thread_sut.start()
    mock_monologue_serv.get_monologue_by_id.return_value.status = (
        MonologueStatus.FAILURE
    )

    thread_sut.join()

    # Assert
    mock_on_finish.assert_called_once_with(thread_sut)


def test_agentic_thread_calls_on_finish_when_crashing_and_marks_monologue_as_failed(
    thread_sut, mock_monologue_serv, mock_on_finish
):
    # Arrange
    mock_monologue_serv.get_monologue_by_id.side_effect = NonexistentMonologueError(99)

    # Act
    thread_sut.start()
    thread_sut.join()

    # Assert
    mock_monologue_serv.set_monologue_status.assert_called_once_with(
        1, MonologueStatus.FAILURE
    )
    mock_on_finish.assert_called_once_with(thread_sut)
