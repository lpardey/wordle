from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str = "Guillermo"
    password: str = "12345"
    can_play: bool = True
