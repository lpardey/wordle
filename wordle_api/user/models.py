from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    # en verdad nunca querremos guardar passwords en texto plano
    # pero de momento en este ejemplo vamos a ir tirando con eso
    password: str


class UserSession(BaseModel):
    session_id: int
    user_id: int
    token: str
    expiration_date: datetime
