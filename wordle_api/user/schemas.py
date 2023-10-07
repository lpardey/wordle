from pydantic import BaseModel
from datetime import datetime


class AuthenticatedRequest(BaseModel):
    token: str


class SignUpRequest(BaseModel):
    username: str
    password: str


class SignUpResponse(BaseModel):
    user_id: int


class UpdateRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_id: int
    user_id: int
    token: str
    session_creation_date: datetime
