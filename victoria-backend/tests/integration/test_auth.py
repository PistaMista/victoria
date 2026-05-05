import pytest
from unittest.mock import patch
from sqlalchemy import insert, select
from app.model.user import User, Role


@pytest.mark.parametrize(
    "username,password",
    [
        ("John", "mypass123"),  # wrong password
        ("Thomas", "actual"),  # wrong username
        ("Thomas", "mypass123"),  # both wrong
    ],
)
def test_invalid_login_responds_with_401_and_error(
    db_session, client, username, password
):
    # Arrange
    user = User(
        username="John",
        password_hash=b"$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa".decode(
            "utf-8"
        ),
        role=Role.ADMIN,
    )
    db_session.add(user)
    db_session.flush()

    # Act
    res = client.post(
        "/api/auth/login", json={"username": username, "password": password}
    )

    # Assert
    assert res.status_code == 401
    assert res.json() == {"detail": "Invalid credentials"}


@patch("time.time", return_value=1753211036)
def test_valid_login_responds_with_200_and_sets_jwt_cookie(
    mock_time, client, db_session
):
    # Arrange
    user = User(
        id=1,
        username="John",
        password_hash=b"$2b$12$o8CqurHMoPKWzga2oohzdu0zpukOChhEdEdSBZO1hCZAeRyl5jtJa".decode(
            "utf-8"
        ),
        role=Role.ADMIN,
    )
    db_session.add(user)
    db_session.flush()

    # Act
    res = client.post(
        "/api/auth/login", json={"username": "John", "password": "actual"}
    )
    set_cookie_header = res.headers.get("set-cookie")

    # Assert
    assert res.status_code == 200
    assert set_cookie_header is not None
    assert "HttpOnly" in set_cookie_header
    assert "SameSite=strict" in set_cookie_header
    assert "token" in client.cookies
    assert (
        client.cookies["token"]
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJpc3N1ZWQiOjE3NTMyMTEwMzYsImV4cGlyZXMiOjE3NTU4MDMwMzZ9.jPFEGbfJMQ63T70_vMPBMtcn8COey3U9JU1Ch3XvXT0"
    )


def test_protected_endpoint_responds_with_401_when_not_logged_in(client):
    # Arrange

    # Act
    res = client.get("/api/auth/me")

    # Assert
    assert res.status_code == 401


@patch("time.time", return_value=9999999999999999999999999)
def test_protected_endpoint_responds_with_401_when_token_expired(
    mock_time, admin_client
):
    # Arrange

    # Act
    res = admin_client.get("/api/auth/me")

    # Assert
    assert res.status_code == 401


def test_protected_endpoint_responds_with_401_when_token_invalid(admin_client):
    # Arrange

    # Act
    res = admin_client.get("/api/auth/me", cookies={"token": "tokenito"})

    # Assert
    assert res.status_code == 401


def test_me_endpoint_responds_with_200_and_user_info_when_logged_in(user_client):
    # Arrange

    # Act
    res = user_client.get("/api/auth/me")

    # Assert
    assert res.status_code == 200
    assert res.json() == {"username": "user", "role": "user"}


def test_admin_endpoint_responds_with_403_when_not_admin(user_client):
    # Arrange

    # Act
    res = user_client.get("/api/auth/me/admin")

    # Assert
    assert res.status_code == 403


def test_admin_endpoint_responds_with_200_when_admin(admin_client):
    # Arrange

    # Act
    res = admin_client.get("/api/auth/me/admin")

    # Assert
    assert res.status_code == 200


def test_register_creates_new_user_in_database(client, db_session):
    # Arrange

    # Act
    res = client.post(
        "/api/auth/register", json={"username": "John", "password": "lol"}
    )

    # Assert
    new_user = db_session.query(User).where(User.username == "John").first()

    assert res.status_code == 200
    assert new_user.username == "John"


def test_register_does_not_create_new_user_if_username_empty(client, db_session):
    # Arrange

    # Act
    res = client.post("/api/auth/register", json={"username": "", "password": "mypass"})

    # Assert
    assert res.status_code == 422
    assert db_session.query(User).first() is None


def test_register_does_not_create_new_user_if_password_empty(client, db_session):
    # Arrange

    # Act
    res = client.post("/api/auth/register", json={"username": "user", "password": ""})

    # Assert
    assert res.status_code == 422
    assert db_session.query(User).first() is None


def test_register_does_not_create_new_user_if_username_taken(client, db_session):
    # Arrange
    user = User(username="taken", password_hash="asdasdasd", role=Role.ADMIN)
    db_session.add(user)
    db_session.flush()

    # Act
    res = client.post(
        "/api/auth/register", json={"username": "taken", "password": "lol"}
    )

    # Assert
    assert res.status_code == 400
    assert db_session.query(User).count() == 1


def test_first_registered_user_is_automatically_admin(client, db_session):
    # Arrange
    assert db_session.scalars(select(User)).first() is None

    # Act
    client.post(
        "/api/auth/register", json={"username": "alice", "password": "porcodio"}
    )

    # Assert
    user = db_session.scalars(select(User).where(User.username == "alice")).first()

    assert user is not None
    assert user.role == Role.ADMIN


def test_subsequent_registered_users_are_normal_users(client, db_session):
    # Arrange
    existing_user = User(username="exists", password_hash="dasdasdasd", role=Role.ADMIN)
    db_session.add(existing_user)
    db_session.flush()

    # Act
    client.post(
        "/api/auth/register", json={"username": "alice", "password": "porcodio"}
    )

    # Assert
    user = db_session.scalars(select(User).where(User.username == "alice")).first()

    assert user is not None
    assert user.role == Role.USER
