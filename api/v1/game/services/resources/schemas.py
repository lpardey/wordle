# Standard Library
from enum import Enum, IntEnum


class GameResult(str, Enum):
    VICTORY = "VICTORY"
    DEFEAT = "DEFEAT"


class GuessResult(str, Enum):
    GUESSED = "GUESSED"
    NOT_GUESSED = "NOT_GUESSED"


class GameStatus(str, Enum):
    WAITING_FOR_GUESS = "WAITING_FOR_GUESS"
    FINISHED = "FINISHED"


class GameDifficulty(str, Enum):
    NORMAL = "NORMAL"
    HARD = "HARD"


class LetterStatus(IntEnum):
    IN_PLACE = 0
    PRESENT = 1
    NOT_PRESENT = 2
    PRESENT_REPEATED = 3
