# Standard Library
from datetime import datetime
from enum import Enum
from typing import TypedDict
from uuid import UUID

# Dependencies
from pydantic import BaseModel

# From apps
from api.v1.game.services.resources.schemas import GameDifficulty, GameResult, GameStatus, GuessResult, LetterStatus


class BasicStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"


class BasicResponse(BaseModel):
    status: BasicStatus = BasicStatus.OK
    message: str | None = None


class GameConfig(BaseModel):
    number_of_attempts: int = 6
    game_difficulty: GameDifficulty = GameDifficulty.NORMAL


class GuessSchema(TypedDict):
    guess: str
    letters_status: list[LetterStatus]


class GameStatusResponse(BaseModel):
    id: UUID
    _game_word: str
    guesses_left: int
    status: GameStatus
    difficulty: GameDifficulty
    creation_date: datetime
    guesses: list[GuessSchema]
    result: GameResult | None
    ongoing: bool
    finished_date: datetime | None


class GameState(BaseModel):
    id: UUID
    game_word: str
    guess: str
    status: GameStatus
    result: GameResult | None


class CreateGameRequest(BaseModel):
    user_id: UUID
    game_config: GameConfig = GameConfig()


class CreateGameResponse(BaseModel):
    game_id: UUID
    creation_date: datetime


class TakeAGuessRequest(BaseModel):
    guess: str


class TakeAGuessResponse(BasicResponse):
    status: BasicStatus
    message: str | None
    guess_result: GuessResult | None
    letters_status: list[LetterStatus] | None


class LastGameResponse(BaseModel):
    game_id: UUID
    game_word: str
    ongoing: bool
    finished_date: datetime | None
