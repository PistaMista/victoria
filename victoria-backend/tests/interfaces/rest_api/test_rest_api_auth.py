import pytest
from fastapi import status
from app.services.auth import InvalidLoginError
from app.services.user import UserExistsError
from app.model.user import Role

def test_login_calls_auth_service_correctly(mock_client, auth_mock):
    # Arrange
    
    # Act
    mock_client.post('/api/auth/login', json={
        'username': "usernamos",
        'password': "passwordito"
    })
    
    # Assert
    auth_mock.get_login_token.assert_called_once_with(
        "usernamos", "passwordito"
    )

def test_login_responds_with_401_on_invalid_login(mock_client, auth_mock):
    # Arrange
    auth_mock.get_login_token.side_effect = InvalidLoginError()
    
    # Act
    res = mock_client.post('/api/auth/login', json={
        'username': "usernamos",
        'password': "passwordito"
    })
    
    # Assert
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    

def test_login_sets_jwt_cookie_on_valid_login(mock_client, auth_mock):
    # Arrange
    auth_mock.get_login_token.return_value = "tokenito"

    # Act
    res = mock_client.post('/api/auth/login', json={
        'username': "usernamos",
        'password': "passwordito"
    })
    set_cookie_header = res.headers.get("set-cookie")
    
    # Assert
    assert res.status_code == 200
    assert set_cookie_header is not None
    assert "HttpOnly" in set_cookie_header
    assert "SameSite=strict" in set_cookie_header
    assert "token" in mock_client.cookies
    assert mock_client.cookies["token"] == "tokenito"
    
def test_register_creates_admin_user_when_no_user_exists(mock_client, user_mock):
    # Arrange
    user_mock.is_any_user_registered.return_value = False
    
    # Act
    mock_client.post('/api/auth/register', json={
        'username': "usernamos",
        'password': "passwordito"
    })
    
    # Assert
    user_mock.create_user.assert_called_once_with(
        username="usernamos",
        password="passwordito",
        role=Role.ADMIN
    )
    
def test_register_creates_normal_user_when_another_user_exists(mock_client, user_mock):
    # Arrange
    user_mock.is_any_user_registered.return_value = True
    
    # Act
    mock_client.post('/api/auth/register', json={
        'username': "usernamos",
        'password': "passwordito"
    })
    
    # Assert
    user_mock.create_user.assert_called_once_with(
        username="usernamos",
        password="passwordito",
        role=Role.USER
    )

def test_register_responds_with_400_when_user_exists(mock_client, user_mock):
    # Arrange
    user_mock.create_user.side_effect = UserExistsError("usernamos")
    
    # Act
    res = mock_client.post('/api/auth/register', json={
        'username': "usernamos",
        'password': "passwordito"
    })
    
    # Assert
    assert res.status_code == status.HTTP_400_BAD_REQUEST
        
def test_me_calls_auth_service_correctly(mock_client, auth_mock):
    # Arrange
    
    # Act
    try:
        mock_client.get('/api/auth/me', cookies={
            "token": "tokenito"
        })
    except:
        pass
    
    # Assert
    auth_mock.get_as_non_admin_user.assert_called_once_with("tokenito")

def test_me_admin_calls_auth_service_correctly(mock_client, auth_mock):
    # Arrange
    
    # Act
    try:
        mock_client.get('/api/auth/me/admin', cookies={
            "token": "tokenito"
        })
    except:
        pass
    
    # Assert
    auth_mock.get_as_admin_user.assert_called_once_with("tokenito")