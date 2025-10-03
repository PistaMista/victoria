from app.services.trigger import NonexistentTriggerError, TriggerDiff, TimerTriggerDiff, PollTriggerDiff, ChatTriggerDiff, WebhookTriggerDiff
from app.services.auth import NotLoggedInError, AdminRequiredError
from app.model.trigger import TimerTrigger, PollTrigger, ChatTrigger, WebhookTrigger
from fastapi import status

def test_list_triggers_for_user_returns_200_and_list_of_allowed_triggers_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()
    trigger_mock.get_user_allowed_triggers.return_value = [
        TimerTrigger(
            id=1,
            name="Start task",
            template="Pick a task and do it",
            interval=200
        ),
        PollTrigger(
            id=2,
            name="Check news",
            template="Latest news: $(content)",
            interval=200
        )
    ]

    # Act
    res = mock_client.get(
        "/api/triggers"
    )

    # Assert
    trigger_mock.get_user_allowed_triggers(
        user_id=1
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 1,
            "name": "Start task",
            "type": "timer"
        },
        {
            "id": 2,
            "name": "Check news",
            "type": "poll"
        }
    ]

def test_list_triggers_for_user_returns_401_when_not_logged_in(mock_client, auth_mock, trigger_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/triggers"
    )

    # Assert
    trigger_mock.get_user_allowed_triggers.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_all_triggers_returns_200_and_list_of_all_triggers_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_all_triggers.return_value = [
        ChatTrigger(
            id=3,
            name="Start task",
            template="Pick a task and do it",
            receiver="research"
        ),
        WebhookTrigger(
            id=4,
            name="Check news",
            template="Latest news: $(content)",
            endpoint="/endpoint"
        )
    ]

    # Act
    res = mock_client.get(
        "/api/triggers/all"
    )

    # Assert
    trigger_mock.get_all_triggers.assert_called_with()
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [
        {
            "id": 3,
            "name": "Start task",
            "type": "chat"
        },
        {
            "id": 4,
            "name": "Check news",
            "type": "webhook"
        }
    ]

def test_list_all_triggers_returns_401_when_not_logged_in(mock_client, auth_mock, trigger_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/triggers/all"
    )

    # Assert
    trigger_mock.get_all_triggers.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_all_triggers_returns_403_when_not_admin(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get(
        "/api/triggers/all"
    )

    # Assert
    trigger_mock.get_all_triggers.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_create_trigger_returns_200_and_creates_timer_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = TimerTrigger(
        id=3,
        name="Start task",
        template="Pick a task",
        interval=100
    )

    # Act
    res = mock_client.post(
        "/api/triggers",
        json={
            "name": "Start task",
            "template": "Pick a task",
            "parser": "identity",
            "settings": {
                "type": "timer",
                "interval": 100
            }
        }
    )

    # Assert
    trigger_mock.add_timer_trigger.assert_called_with(
        name="Start task",
        template="Pick a task",
        interval=100
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 3,
        "name": "Start task",
        "type": "timer"
    }

def test_create_trigger_returns_200_and_creates_poll_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = PollTrigger(
        id=3,
        name="Check news",
        template="Latest news: $(content)",
        interval=100,
        url="novinky.cz"
    )

    # Act
    res = mock_client.post(
        "/api/triggers",
        json={
            "name": "Check news",
            "template": "Latest news: $(content)",
            "parser": "identity",
            "settings": {
                "type": "poll",
                "interval": 100,
                "url": "novinky.cz"
            }
        }
    )

    # Assert
    trigger_mock.add_poll_trigger.assert_called_with(
        name="Check news",
        template="Latest news: $(content)",
        interval=100,
        url="novinky.cz"
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 3,
        "name": "Check news",
        "type": "poll"
    }

def test_create_trigger_returns_200_and_creates_chat_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = ChatTrigger(
        id=3,
        name="Maintenance chat",
        template="New message",
        receiver="maintenance",
    )

    # Act
    res = mock_client.post(
        "/api/triggers",
        json={
            "name": "Maintenance chat",
            "template": "New message",
            "parser": "identity",
            "settings": {
                "type": "chat",
                "receiver": "maintenance"
            }
        }
    )

    # Assert
    trigger_mock.add_chat_trigger.assert_called_with(
        name="Maintenance chat",
        template="New message",
        receiver="maintenance"
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 3,
        "name": "Maintenance chat",
        "type": "chat"
    }

def test_create_trigger_returns_200_and_creates_webhook_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = WebhookTrigger(
        id=3,
        name="Discord message received",
        template="DC message",
        endpoint="/discord",
    )

    # Act
    res = mock_client.post(
        "/api/triggers",
        json={
            "name": "Discord message received",
            "template": "DC message",
            "parser": "identity",
            "settings": {
                "type": "webhook",
                "url": "/discord"
            }
        }
    )

    # Assert
    trigger_mock.add_webhook_trigger.assert_called_with(
        name="Discord message received",
        template="DC message",
        endpoint="/discord"
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 3,
        "name": "Discord message received",
        "type": "webhook"
    }

def test_create_trigger_returns_401_when_not_logged_in(mock_client, auth_mock, trigger_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.post(
        "/api/triggers",
        json={
            "name": "Discord message received",
            "template": "DC message",
            "parser": "identity",
            "settings": {
                "type": "webhook",
                "url": "/discord"
            }
        }
    )

    # Assert
    trigger_mock.add_timer_trigger.assert_not_called()
    trigger_mock.add_poll_trigger.assert_not_called()
    trigger_mock.add_chat_trigger.assert_not_called()
    trigger_mock.add_webhook_trigger.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_trigger_returns_403_when_not_admin(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.post(
        "/api/triggers",
        json={
            "name": "Discord message received",
            "template": "DC message",
            "parser": "identity",
            "settings": {
                "type": "webhook",
                "url": "/discord"
            }
        }
    )

    # Assert
    trigger_mock.add_timer_trigger.assert_not_called()
    trigger_mock.add_poll_trigger.assert_not_called()
    trigger_mock.add_chat_trigger.assert_not_called()
    trigger_mock.add_webhook_trigger.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_get_trigger_returns_200_and_timer_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = TimerTrigger(
        id=10,
        name="Check house inventory",
        template="TEMP",
        interval=39
    )

    # Act
    res = mock_client.get(
        "/api/triggers/10"
    )

    # Assert
    trigger_mock.get_trigger_by_id.assert_called_with(
        id=10
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 10,
        "name": "Check house inventory",
        "parser": "identity",
        "template": "TEMP",
        "settings": {
            "type": "timer",
            "interval": 39
        }
    }

def test_get_trigger_returns_200_and_poll_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = PollTrigger(
        id=101,
        name="Get news",
        template="TEMP",
        interval=39,
        url="seznam.cz"
    )

    # Act
    res = mock_client.get(
        "/api/triggers/101"
    )

    # Assert
    trigger_mock.get_trigger_by_id.assert_called_with(
        id=101
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 101,
        "name": "Get news",
        "template": "TEMP",
        "parser": "identity",
        "settings": {
            "type": "poll",
            "interval": 39,
            "url": "seznam.cz"
        }
    }

def test_get_trigger_returns_200_and_chat_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = ChatTrigger(
        id=21,
        name="Research chat",
        template="New message received",
        receiver="research"
    )

    # Act
    res = mock_client.get(
        "/api/triggers/21"
    )

    # Assert
    trigger_mock.get_trigger_by_id.assert_called_with(
        id=21
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 21,
        "name": "Research chat",
        "template": "New message received",
        "parser": "identity",
        "settings": {
            "type": "chat",
            "receiver": "research"
        }
    }

def test_get_trigger_returns_200_and_webhook_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = WebhookTrigger(
        id=7,
        name="Discord message",
        template="DC message",
        endpoint="/discord"
    )

    # Act
    res = mock_client.get(
        "/api/triggers/7"
    )

    # Assert
    trigger_mock.get_trigger_by_id.assert_called_with(
        id=7
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "id": 7,
        "name": "Discord message",
        "template": "DC message",
        "parser": "identity",
        "settings": {
            "type": "webhook",
            "url": "/discord"
        }
    }

def test_get_trigger_returns_401_when_not_logged_in(mock_client, auth_mock, trigger_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.get(
        "/api/triggers/70"
    )

    # Assert
    trigger_mock.get_trigger_by_id.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_trigger_returns_403_when_not_admin(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.get(
        "/api/triggers/70"
    )

    # Assert
    trigger_mock.get_trigger_by_id.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_get_trigger_returns_404_for_nonexistent_trigger(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.side_effect = NonexistentTriggerError(92)

    # Act
    res = mock_client.get(
        "/api/triggers/92"
    )

    # Assert
    trigger_mock.get_trigger_by_id.assert_called_with(
        id=92
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_update_trigger_returns_200_and_updates_base_trigger_attributes_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = ChatTrigger(
        id=57,
        name="Something",
        template="lol",
        receiver="technical"
    )

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "name": "wooo",
            "template": "new"
        }
    )

    # Assert
    assert res.status_code == status.HTTP_200_OK
    trigger_mock.update_trigger.assert_called_with(
        trigger_id=57,
        changes=TriggerDiff(
            name="wooo",
            template="new"
        )
    )

def test_update_trigger_returns_200_and_updates_timer_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = TimerTrigger(
        name="",
        template="",
        interval=50
    )

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "name": "o",
            "settings": {
                "interval": 300
            }
        }
    )

    # Assert
    assert res.status_code == status.HTTP_200_OK
    trigger_mock.update_trigger.assert_called_with(
        trigger_id=57,
        changes=TimerTriggerDiff(
            name="o",
            interval=300
        )
    )

def test_update_trigger_returns_200_and_updates_poll_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = PollTrigger(
        name="Get upcoming events",
        template="template",
        interval=50
    )

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "name": "no",
            "settings": {
                "interval": 150
            }
        }
    )

    # Assert
    trigger_mock.update_trigger.assert_called_with(
        trigger_id=57,
        changes=PollTriggerDiff(
            name="no",
            interval=150
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_update_trigger_returns_200_and_updates_chat_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = ChatTrigger(
        name="General chat",
        template="template",
        receiver="general"
    )

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "template": "woo",
            "settings": {
                "receiver": "lol"
            }
        }
    )

    # Assert
    trigger_mock.update_trigger.assert_called_with(
        trigger_id=57,
        changes=ChatTriggerDiff(
            template="woo",
            receiver="lol"
        )
    )
    assert res.status_code == status.HTTP_200_OK

def test_update_trigger_returns_200_and_updates_webhook_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = WebhookTrigger(
        name="Webhook",
        template="template",
        endpoint="/hook"
    )

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "template": "woo",
            "settings": {
                "url": "/discord"
            }
        }
    )

    # Assert
    assert res.status_code == status.HTTP_200_OK
    trigger_mock.update_trigger.assert_called_with(
        trigger_id=57,
        changes=WebhookTriggerDiff(
            template="woo",
            endpoint="/discord"
        )
    )

def test_update_trigger_returns_200_and_changes_trigger_type_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.get_trigger_by_id.return_value = ChatTrigger(
        name="General chat",
        template="template",
        receiver="general"
    )

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "settings": {
                "type": "webhook"
            }
        }
    )

    # Assert
    trigger_mock.update_trigger.assert_called_with(
        trigger_id=57,
        changes=WebhookTriggerDiff()
    )
    assert res.status_code == status.HTTP_200_OK

def test_update_trigger_returns_401_when_not_logged_in(mock_client, auth_mock, trigger_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "settings": {
                "type": "webhook"
            }
        }
    )

    # Assert
    trigger_mock.update_trigger.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_trigger_returns_403_when_not_admin(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.put(
        "/api/triggers/60",
        json={
            "settings": {
                "receiver": "lol"
            }
        }
    )

    # Assert
    trigger_mock.update_trigger.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_trigger_returns_404_for_nonexistent_trigger(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.update_trigger.side_effect = NonexistentTriggerError(60)

    # Act
    res = mock_client.put(
        "/api/triggers/57",
        json={
            "settings": {
                "type": "webhook"
            }
        }
    )

    # Assert
    trigger_mock.update_trigger.assert_called_with(
        trigger_id=57,
        changes=WebhookTriggerDiff()
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_trigger_returns_200_and_deletes_trigger_on_valid_request(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user

    # Act
    res = mock_client.delete(
        "/api/triggers/60"
    )

    # Assert
    trigger_mock.remove_trigger.assert_called_with(
        id=60
    )
    assert res.status_code == status.HTTP_200_OK

def test_delete_trigger_returns_401_when_not_logged_in(mock_client, auth_mock, trigger_mock):
    # Arrange
    auth_mock.get_as_non_admin_user.side_effect = NotLoggedInError()
    auth_mock.get_as_admin_user.side_effect = NotLoggedInError()

    # Act
    res = mock_client.delete(
        "/api/triggers/60"
    )

    # Assert
    trigger_mock.remove_trigger.assert_not_called()
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_trigger_returns_403_when_not_admin(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.side_effect = AdminRequiredError()

    # Act
    res = mock_client.delete(
        "/api/triggers/60"
    )

    # Assert
    trigger_mock.remove_trigger.assert_not_called()
    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_delete_trigger_returns_404_for_nonexistent_trigger(mock_client, auth_mock, trigger_mock, user):
    # Arrange
    auth_mock.get_as_non_admin_user.return_value = user
    auth_mock.get_as_admin_user.return_value = user
    trigger_mock.remove_trigger.side_effect = NonexistentTriggerError(30)

    # Act
    res = mock_client.delete(
        "/api/triggers/30"
    )

    # Assert
    trigger_mock.remove_trigger.assert_called_with(
        id=30
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
