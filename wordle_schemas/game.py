from enum import Enum
from pydantic import BaseModel

class GameCreationResponse(BaseModel):
    game_id: int
    username: str


class GameStatus(str, Enum):
    AVAILABLE_TO_PLAY = "AVAILABLE_TO_PLAY"
    WAITING_FOR_GUESS = "WAITING_FOR_GUESS"
    NOT_AVAILABLE_TO_PLAY = "NOT_AVAILABLE_TO_PLAY"


class GameConfig(BaseModel):
    number_of_attempts: int = 6
    game_mode: str = "Normal"

