from pydantic import BaseModel
from datetime import datetime


class AuthenticatedRequest(BaseModel):
    token: str


class SignUpRequest(BaseModel):
    username: str
    password: str


class SignUpResponse(BaseModel):
    player_id: int


class UpdateRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    player_id: int
    session_id: int
    token: str
    session_creation_date: datetime
    session_expiration_date: datetime
