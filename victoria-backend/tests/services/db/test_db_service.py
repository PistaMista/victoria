import pytest
from app.services.db import DatabaseService
from app.model.user import User, Role
from sqlalchemy import select

@pytest.fixture(scope="function")
def serv(db_container):
    return DatabaseService(db_url=db_container)

def test_database_service_provides_session_factory(serv):
    # Arrange
    
    # Act 
    with serv.session() as session:
        res = session.scalars(
            select(User).where(User.username == "user")
        ).first()
        
        # Assert
        assert res is None

def test_database_service_can_run_migrations(db_container):
    # The migrations are run once during test setup,
    # so if they fail, the whole test suite fails.

    # Assert
    assert True
