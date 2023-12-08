# Standard Library
from enum import IntEnum, StrEnum


class GameResult(StrEnum):
    VICTORY = "VICTORY"
    DEFEAT = "DEFEAT"


class GuessResult(StrEnum):
    GUESSED = "GUESSED"
    NOT_GUESSED = "NOT_GUESSED"


class GameStatus(StrEnum):
    WAITING_FOR_GUESS = "WAITING_FOR_GUESS"
    FINISHED = "FINISHED"


class GameDifficulty(StrEnum):
    NORMAL = "NORMAL"
    HARD = "HARD"


class LetterStatus(IntEnum):
    IN_PLACE = 0
    PRESENT = 1
    NOT_PRESENT = 2
