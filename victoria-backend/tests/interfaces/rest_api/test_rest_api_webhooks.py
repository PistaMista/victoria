from app.services.trigger import InvalidWebhookEndpointError
from fastapi import status

def test_webhook_endpoints_return_200_and_call_webhook_service_for_valid_webhook_endpoint(mock_client, trigger_mock):
    # Arrange

    # Act
    res = mock_client.post(
            "/api/webhooks/coolendpoint/p",
            content="lol"    
    )

    # Assert
    trigger_mock.receive_webhook_payload.assert_called_with(
        endpoint="coolendpoint/p",
        content="lol"
    )
    assert res.status_code == status.HTTP_200_OK

def test_webhook_endpoints_return_404_for_invalid_webhook_endpoint(mock_client, trigger_mock):
    # Arrange
    trigger_mock.receive_webhook_payload.side_effect = InvalidWebhookEndpointError("coolendpoint")

    # Act
    res = mock_client.post(
            "/api/webhooks/coolendpoint",
            content="lol"    
    )

    # Assert
    trigger_mock.receive_webhook_payload.assert_called_with(
        endpoint="coolendpoint",
        content="lol"
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
