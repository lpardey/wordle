from pydantic import BaseModel, SecretStr
from datetime import datetime


class SignUpRequest(BaseModel):
    username: str
    password: SecretStr


class SignUpResponse(BaseModel):
    user_id: int


class LoginResponse(BaseModel):
    session_id: int
    user_id: int
    access_token: str
    token_type:str
    session_creation_date: datetime