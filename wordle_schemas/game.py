from enum import Enum
from pydantic import BaseModel
from w_game.game import GameStatistics, GameStatus, Guess, WordleLetters


class BasicStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"


class BasicResponse(BaseModel):
    status: BasicStatus = BasicStatus.OK
    message: str | None = None


class GameCreationResponse(BaseModel):
    game_id: int
    username: str


class GameConfig(BaseModel):
    number_of_attempts: int = 6
    game_mode: str = "Normal"


class GameStatusInfo(BaseModel):
    current_guess: Guess
    guess_letters: WordleLetters
    game_status: GameStatus


class GameStatusResponse(BasicResponse):
    game_status_info: GameStatusInfo


class GameStatisticsResponse(BaseModel):
    game_statistics: GameStatistics
