# Standard Library
from datetime import datetime
from uuid import UUID

# Dependencies
from pydantic import BaseModel, SecretStr


class CreateUserRequest(BaseModel):
    username: str
    password: SecretStr


class CreateUserResponse(BaseModel):
    user_id: UUID
    username: str
    disabled: bool
    creation_date: datetime


class LoginResponse(BaseModel):
    session_id: UUID
    user_id: UUID
    access_token: str
    token_type: str
    session_creation_date: datetime
