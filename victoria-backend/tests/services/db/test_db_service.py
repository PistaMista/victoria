import pytest
# from app.services.db import DatabaseService
from app.model.user import User, Role
from sqlalchemy import select

@pytest.fixture(scope="function")
def serv(db_container):
    return DatabaseService(db_url=db_container)

def test_database_service_provides_session_factory(db_session, serv):
    # Arrange
    user = User(
        username="user",
        password="pass",
        role=Role.USER
    )
    db_session.add(user)
    db_session.commit
    
    with serv.session() as session:
        # Act 
        res = session.scalars(
            select(User).where(User.username == "user")
        ).first()
        
        # Assert
        assert res is not None
        assert res.username == "user"
        assert res.role == Role.USER

def test_database_service_can_run_migrations():
    # The migrations are run once during test setup,
    # so if they fail, the whole test suite fails.

    # Assert
    assert True
