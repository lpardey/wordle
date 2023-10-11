from enum import Enum


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
