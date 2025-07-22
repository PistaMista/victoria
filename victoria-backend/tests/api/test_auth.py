from sqlalchemy import insert
from app.model.user import User
from pytest import mark

def test_invalid_login_responds_with_401():
    assert False

def test_valid_login_responds_with_jwt_token():
    assert False

def test_register_creates_new_user_in_database():
    assert False

def test_register_does_not_create_new_user_if_username_empty():
    assert False

def test_register_does_not_create_new_user_if_password_empty():
    assert False
    
def test_register_does_not_create_new_user_if_username_taken():
    assert False
    