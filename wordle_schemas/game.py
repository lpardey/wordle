from enum import Enum
from pydantic import BaseModel
from wordle_game.game import GameStatus
from wordle_game.game_state import GameDifficulty, GuessResult

# schema = transferir informacion --- esto va en la API
# modelo = almacenar informacion --- esto va en la base de datos


class BasicStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"


class BasicResponse(BaseModel):
    status: BasicStatus = BasicStatus.OK
    message: str | None = None


class GameCreationResponse(BaseModel):
    game_id: int


class GameConfig(BaseModel):
    number_of_attempts: int = 6
    game_difficulty: GameDifficulty = GameDifficulty.NORMAL


class GameStatusInfo(BaseModel):
    game_word: str
    guesses: list[str]
    game_status: GameStatus
    difficulty: GameDifficulty


class GameStatusResponse(BasicResponse):
    game_status_info: GameStatusInfo


class TakeAGuessRequest(BaseModel):
    guess: str


class TakeAGuessResponse(BasicResponse):
    guess_result: GuessResult
