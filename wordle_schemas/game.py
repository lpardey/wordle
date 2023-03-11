from enum import Enum
from pydantic import BaseModel

from wordle.game.router import PlayerState


class GameCreationResponse(BaseModel):
    game: dict[PlayerState: int]

class GameStatus(str, Enum):
    AVAILABLE_TO_PLAY = "AVAILABLE_TO_PLAY"
    WAITING_FOR_GUESS = "WAITING_FOR_GUESS"
    NOT_AVAILABLE_TO_PLAY = "NOT_AVAILABLE_TO_PLAY"