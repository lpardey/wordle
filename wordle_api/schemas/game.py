from enum import Enum
from pydantic import BaseModel
from wordle_api.services.resources.schemas import GameDifficulty, GameResult, GameStatus, GuessResult, LetterStatus
from datetime import datetime

# schema = transferir informacion --- esto va en la API
# modelo = almacenar informacion --- esto va en la base de datos


class BasicStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"


class BasicResponse(BaseModel):
    status: BasicStatus = BasicStatus.OK
    message: str | None = None


class GameConfig(BaseModel):
    number_of_attempts: int = 6
    game_difficulty: GameDifficulty = GameDifficulty.NORMAL


class GameStatusResponse(BaseModel):
    id: int
    _game_word: str
    guesses_left: int
    status: GameStatus
    result: GameResult | None
    difficulty: GameDifficulty
    guesses: list[str]
    creation_date: datetime


class CreateGameRequest(BaseModel):
    user_id: int
    game_config: GameConfig = GameConfig()


class CreateGameResponse(BaseModel):
    game_id: int


class TakeAGuessRequest(BaseModel):
    guess: str


class TakeAGuessResponse(BasicResponse):
    status: BasicStatus
    message: str | None
    guess_result: GuessResult | None
    guess_letters_status: list[LetterStatus] | None
