from pydantic import BaseModel


class AuthenticatedRequest(BaseModel):
    token: str


class SignUpRequest(BaseModel):
    username: str
    password: str


class UpdateRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
