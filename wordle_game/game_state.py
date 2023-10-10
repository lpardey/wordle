from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class GameResult(str, Enum):
    VICTORY = "VICTORY"
    DEFEAT = "DEFEAT"


class GuessResult(str, Enum):
    GUESSED = "GUESSED"
    NOT_GUESSED = "NOT_GUESSED"


class GameStatus(str, Enum):
    WAITING_FOR_GUESS = "WAITING_FOR_GUESS"
    FINISHED = "FINISHED"


class GameDifficulty(int, Enum):
    NORMAL = 0
    HARD = 1


class LetterStatus(int, Enum):
    IN_PLACE = 0
    PRESENT = 1
    NOT_PRESENT = 2


class GameState(BaseModel):
    player_id: int
    game_word: str
    guesses: list[str] = []
    number_of_attempts: int = 6
    result: GameResult | None = GameResult.DEFEAT
    difficulty: GameDifficulty = GameDifficulty.NORMAL
    game_creation_date: datetime

    @property
    def guesses_left(self) -> int:
        return self.number_of_attempts - len(self.guesses)

    @property
    def status(self) -> GameStatus:
        if self.guesses_left > 0 and self.result != GameResult.VICTORY:
            return GameStatus.WAITING_FOR_GUESS
        return GameStatus.FINISHED
