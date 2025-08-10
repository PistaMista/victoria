import pytest
from unittest import mock
from app.model.user import User, Role
# from app.services.user import UserService
# from app.services.auth import AuthService, InvalidLoginError, ExpiredLoginError, AdminRequiredError


@pytest.fixture(scope="function")
def auth_serv():
    user_serv_mock = mock.Mock(spec=UserService)
    user_serv_mock.get_user_by_id.side_effect = lambda id: {
        1: User(
            username="John",
            password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
            role=Role.ADMIN
        ),
        2: User(
            username="tom",
            password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
            role=Role.USER
        )
    }.get(id)

    return AuthService(user_service=user_serv_mock)

@mock.patch('time.time', return_value=1753211036)
def test_auth_service_returns_jwt_token_with_valid_login(auth_serv):
    # Arrange
    
    # Act
    token = auth_serv.get_login_token(
        username="John",
        password="actual"
    )
    
    # Assert
    assert token == ""

@pytest.mark.parametrize("username,password", [
    ("John", "wrong"), # wrong password
    ("sdasd", "actual"), # wrong username
    ("sdasd", "wrong") # both wrong
])
def test_auth_service_raises_error_when_getting_token_with_invalid_login(auth_serv, username, password):
    # Arrange

    # Act / Assert
    with pytest.raises(InvalidLoginError):
        auth_serv.get_login_token(
            username=username,
            password=password
        )


@mock.patch('time.time', return_value=1753211036)
def test_auth_service_verifies_valid_nonadmin_token(auth_serv):
    # Arrange
    token = ""

    # Act
    user = auth_serv.get_as_non_admin_user(token)
    
    # Assert
    assert user.username == "tom"
    assert user.role == Role.USER

@mock.patch('time.time', return_value=1753211036)
def test_auth_service_verifies_valid_admin_token(auth_serv):
    # Arrange
    token = ""

    # Act
    user = auth_serv.get_as_non_admin_user(token)
    
    # Assert
    assert user.username == "John"
    assert user.role == Role.ADMIN
    

@mock.patch('time.time', return_value=9999999999999999)
def test_auth_service_rejects_expired_session_token():
    # Arrange
    token = ""
    
    # Act / Assert
    with pytest.raises(ExpiredLoginError):
        auth_serv.get_as_non_admin_user(token)
    

def test_auth_service_rejects_nonadmin_token_when_verifying_admin_token():
    # Arrange
    token = ""
    
    # Act / Assert
    with pytest.raises(AdminRequiredError):
        auth_serv.get_as_admin_user(token)