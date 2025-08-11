import pytest
from unittest import mock
from app.model.trigger import Trigger
from app.model.event import Event
from app.model.agent import Agent
from app.model.monologue import Monologue
from app.model.user import User, Role
from app.services.user import UserService
from app.services.auth import AuthService, InvalidLoginError, ExpiredLoginError, AdminRequiredError, NotLoggedInError


@pytest.fixture(scope="function")
def auth_serv():
    john = User(
            id = 1,
            username="John",
            password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
            role=Role.ADMIN
        )
    tom = User(
            id = 2,
            username="tom",
            password_hash=b'$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa'.decode('utf-8'),
            role=Role.USER
        )
    user_serv_mock = mock.Mock(spec=UserService)
    user_serv_mock.get_user_by_name.side_effect = lambda name: {
        "John": john,
        "tom": tom
    }.get(name)
    user_serv_mock.get_user_by_id.side_effect = lambda id: {
        1: john,
        2: tom
    }.get(id)

    return AuthService(
        user_service=user_serv_mock,
        jwt_secret="3185dd631c07a57c691c31b8d07d44f5f0795fbab2db74835d014a639f536a67",
        login_lifetime=2592000
    )

@mock.patch('time.time', return_value=1753211036)
def test_auth_service_returns_jwt_token_with_valid_login(time, auth_serv):
    # Arrange
    
    # Act
    token = auth_serv.get_login_token(
        username="John",
        password="actual"
    )
    
    # Assert
    assert token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJpc3N1ZWQiOjE3NTMyMTEwMzYsImV4cGlyZXMiOjE3NTU4MDMwMzZ9.SO2nJ4lBOv-kVBpw8iZOHIsg_idRrNQDc1ufU8VKPmI"

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
def test_auth_service_verifies_valid_nonadmin_token(time, auth_serv):
    # Arrange
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJpc3N1ZWQiOjE3NTMyMTEwMzYsImV4cGlyZXMiOjE3NTU4MDMwMzZ9.SklQhNa7KwHStLH-FEpxtTJd-Ue1qtOMV-m5DswmtQ4"

    # Act
    user = auth_serv.get_as_non_admin_user(token)
    
    # Assert
    assert user.username == "tom"
    assert user.role == Role.USER

@mock.patch('time.time', return_value=1753211036)
def test_auth_service_verifies_valid_admin_token(time, auth_serv):
    # Arrange
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJpc3N1ZWQiOjE3NTMyMTEwMzYsImV4cGlyZXMiOjE3NTU4MDMwMzZ9.SO2nJ4lBOv-kVBpw8iZOHIsg_idRrNQDc1ufU8VKPmI"

    # Act
    user = auth_serv.get_as_admin_user(token)
    
    # Assert
    assert user.username == "John"
    assert user.role == Role.ADMIN
    

@mock.patch('time.time', return_value=9999999999999999)
def test_auth_service_rejects_expired_session_token(time, auth_serv):
    # Arrange
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJpc3N1ZWQiOjE3NTMyMTEwMzYsImV4cGlyZXMiOjE3NTU4MDMwMzZ9.SklQhNa7KwHStLH-FEpxtTJd-Ue1qtOMV-m5DswmtQ4"
    
    # Act / Assert
    with pytest.raises(ExpiredLoginError):
        auth_serv.get_as_non_admin_user(token)
    

def test_auth_service_rejects_None_token(auth_serv):
    # Arrange

    # Act / Assert
    with pytest.raises(NotLoggedInError):
        auth_serv.get_as_non_admin_user(None)

    with pytest.raises(NotLoggedInError):
        auth_serv.get_as_admin_user(None)


def test_auth_service_rejects_nonadmin_token_when_verifying_admin_token(auth_serv):
    # Arrange
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJpc3N1ZWQiOjE3NTMyMTEwMzYsImV4cGlyZXMiOjE3NTU4MDMwMzZ9.SklQhNa7KwHStLH-FEpxtTJd-Ue1qtOMV-m5DswmtQ4"
    
    # Act / Assert
    with pytest.raises(AdminRequiredError):
        auth_serv.get_as_admin_user(token)