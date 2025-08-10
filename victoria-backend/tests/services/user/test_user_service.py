# from app.services.user import UserService, UserExistsError
# from app.services.db import DatabaseService
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from app.model.user import User, Role
import pytest
from unittest import mock

@pytest.fixture(scope="function")
def serv(db_factory):
    db_mock = mock.Mock(spec=DatabaseService)
    db_mock.get_session_factory.return_value = db_factory
    serv = UserService(db_service=db_mock)


def test_user_service_creates_user(serv, db_session):
    # Arrange
    
    # Act
    serv.create_normal_user(
        username="John",
        password="hello"
    )
    
    # Assert
    user = db_session.scalars(
        select(User).where(User.username == "John")
    ).first()

    assert user is not None
    assert user.username == "John"
    assert user.hashed_password == ""
    assert user.role == Role.USER

def test_user_service_creates_admin_user(serv, db_session):
    # Arrange
    
    # Act
    serv.create_admin_user(
        username="John",
        password="hello"
    )
    
    # Assert
    user = db_session.scalars(
        select(User).where(User.username == "John")
    ).first()

    assert user is not None
    assert user.username == "John"
    assert user.hashed_password == ""
    assert user.role == Role.ADMIN

def test_user_service_throws_exception_when_creating_user_with_taken_username(serv, db_session):
    # Arrange
    existing_user = User(
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    with pytest.raises(UserExistsError):
        serv.create_normal_user(
            username="exists",
            password="asdadkjanskjdn"
        )
    
    with pytest.raises(UserExistsError):
        serv.create_admin_user(
            username="exists",
            password="asndkanskjdn"
        )

def test_user_service_reports_when_no_users_are_registered(serv, db_factory):
    # Arrange
    
    # Act / Assert
    assert not serv.is_any_user_registered()
    
def test_user_service_reports_when_any_user_is_registered(serv, db_session):
    # Arrange
    existing_user = User(
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    assert serv.is_any_user_registered()

def test_user_service_gets_user(serv, db_session, db_factory):
    # Arrange
    existing_user = User(
        id=1,
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    user = serv.get_user_by_id(1)
    assert user.username == "exists"
    assert user.password_hash == "dasdasdasd"
    assert user.role == Role.ADMIN


def test_user_service_cannot_get_nonexistent_user(serv, db_session, db_factory):
    # Arrange
    existing_user = User(
        id=2,
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act / Assert
    user = serv.get_user_by_id(1)
    assert user is None

def test_user_service_deletes_user(db_session, serv):
    # Arrange
    existing_user = User(
        id=1,
        username="exists",
        password_hash="dasdasdasd",
        role=Role.ADMIN
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Act
    serv.delete_user_by_id(1)
    
    # Assert
    first_user = db_session.scalars(
        select(User)
    ).first()
    
    assert first_user is None
    assert not serv.is_any_user_registered()

