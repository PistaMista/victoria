from sqlalchemy import insert, select
from app.model.user import User
from pytest import mark
from app.model.user import User

def test_invalid_login_responds_with_401_and_error(db_session, client):
    # Arrange
    user = User(username="John", password_hash="sdasdasd")
    db_session.add(user)
    db_session.flush()
    
    # Act
    res_invalid_password = client.post('/api/auth/login', json={
        'username': "John",
        'password': "mypass123"
    })
    res_invalid_username = client.post('/api/auth/login', json={
        'username': "Thomas",
        'password': "actual"
    })
    res_invalid_both = client.post('/api/auth/login', json={
        'username': "Thomas",
        'password': "mypass123"
    })

    # Assert
    assert res_invalid_password.status_code == 401
    assert res_invalid_username.status_code == 401
    assert res_invalid_both.status_code == 401
    
    assert res_invalid_password.json() == {"error": "Invalid credentials"}
    assert res_invalid_username.json() == {"error": "Invalid credentials"}
    assert res_invalid_both.json() == {"error": "Invalid credentials"}

def test_valid_login_responds_with_200_and_jwt_token(client, db_session):
    # Arrange
    user = User(username="John", password_hash="sdasdasd")
    db_session.add(user)
    db_session.flush()
    
    # Act
    res = client.post('/api/auth/login', json={
        "username": "John",
        "password": "actual"
    })
    
    # Assert
    assert res.status_code == 200
    assert res.json() == "token"


def test_register_creates_new_user_in_database(client, db_session):
    # Arrange

    # Act
    res = client.post('/api/auth/register', json={
        "username": "John",
        "password": "lol"
    })

    # Assert
    new_user = db_session.query(User).where(User.username == "John").first()

    assert res.status_code == 200
    assert new_user.username == "John"
    assert new_user.password_hash == "sdaxdzasdasd"

def test_register_does_not_create_new_user_if_username_empty(client, db_session):
    # Arrange

    # Act
    res = client.post('/api/auth/register', json={
        "username": "",
        "password": "mypass"
    })
    
    # Assert
    assert res.status_code == 400
    assert db_session.query(User).first() is None

def test_register_does_not_create_new_user_if_password_empty(client, db_session):
    # Arrange

    # Act
    res = client.post('/api/auth/register', json={
        "username": "user",
        "password": ""
    })
    
    # Assert
    assert res.status_code == 400
    assert db_session.query(User).first() is None
    
def test_register_does_not_create_new_user_if_username_taken(client, db_session):
    # Arrange
    user = User(username="taken", password_hash="asdasdasd")
    db_session.add(user)
    db_session.flush()

    # Act
    res = client.post('/api/auth/register', json={
        "username": "taken",
        "password": "lol"
    })
    
    # Assert
    assert res.status_code == 400
    assert db_session.query(User).count() == 1
    