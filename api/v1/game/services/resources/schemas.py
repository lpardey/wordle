# Standard Library
from enum import Enum, IntEnum
from typing import Literal


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


type LetterStatusList = list[
    Literal[
        LetterStatus.IN_PLACE,
        LetterStatus.PRESENT,
        LetterStatus.PRESENT_REPEATED,
        LetterStatus.NOT_PRESENT,
    ]
]

type PresentLetterStatus = Literal[LetterStatus.PRESENT, LetterStatus.PRESENT_REPEATED]
