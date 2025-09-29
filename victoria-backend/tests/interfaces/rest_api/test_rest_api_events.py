from fastapi import status
from app.services.trigger import NonexistentEventError
from app.services.auth import NotLoggedInError
from app.model.event import Event
from app.model.trigger import PollTrigger

def test_get_event_returns_200_and_event_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    trigger_mock.get_user_event.return_value = Event(
        trigger=PollTrigger(
            id=10,
            name="lol",
            template="temp",
            url="seznam.cz",
            interval=20
        ),
        trigger_id=10,
        content="Weee",
        dispatched=False
    )

    # Act
    res = mock_client.get("/api/events/5")

    # Assert
    trigger_mock.get_user_event.assert_called_with(
        user_id=1,
        event_id=5
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "triggerId": 10,
        "content": "Weee"
    }


def test_get_event_returns_401_when_not_logged_in(mock_client, auth_mock, trigger_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get("/api/events/5")

    # Assert
    trigger_mock.get_user_event.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_event_returns_404_for_nonexistent_event(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    trigger_mock.get_user_event.side_effect = NonexistentEventError(5)

    # Act
    res = mock_client.get("/api/events/5")

    # Assert
    trigger_mock.get_user_event.assert_called_with(
        user_id=1,
        event_id=5
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
