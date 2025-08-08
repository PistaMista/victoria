from pydantic import BaseModel, constr

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=3)