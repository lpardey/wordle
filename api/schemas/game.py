# Standard Library
from datetime import datetime
from enum import Enum

# Dependencies
from pydantic import BaseModel

# From apps
from api.services.resources.schemas import GameDifficulty, GameResult, GameStatus, GuessResult, LetterStatus


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
    difficulty: GameDifficulty
    creation_date: datetime
    guesses: list[str]
    result: GameResult | None
    finished_date: datetime | None


class GameState(BaseModel):
    id: int
    game_word: str
    guess: str
    status: GameStatus
    result: GameResult | None


class CreateGameRequest(BaseModel):
    user_id: int
    game_config: GameConfig = GameConfig()


class CreateGameResponse(BaseModel):
    game_id: int
    creation_date: datetime


class TakeAGuessRequest(BaseModel):
    guess: str


class TakeAGuessResponse(BasicResponse):
    status: BasicStatus
    message: str | None
    guess_result: GuessResult | None
    letters_status: list[LetterStatus] | None


class OnGoingGameReponse(BaseModel):
    ongoing_game: bool
    game_status: GameStatusResponse | None


class LastGameResponse(BaseModel):
    game_id: int
    game_word: str
    finished_date: datetime | None
