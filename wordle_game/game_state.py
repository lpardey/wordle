from enum import Enum
from pydantic import BaseModel
from string import ascii_uppercase

LETTERS_AVAILABLE = sorted(list(set(ascii_uppercase)))


class User(BaseModel):
    username: str = "Guillermo"
    password: str = "12345"

    # property of user -> STatus Available to play or nor available to play


class PlayerState(BaseModel):
    user: User = User()
    player_guess: str = ""
    attempts_left: int = 6
    current_streak: int = 0
    max_streak: int = 0


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
    user_id: int
    game_word: str
    guesses: list[str] = []
    status: GameStatus = GameStatus.WAITING_FOR_GUESS
    result: GameResult = GameResult.DEFEAT
    difficulty: GameDifficulty = GameDifficulty.NORMAL

    @property
    def guesses_left(self) -> int:
        return 6 - len(self.guesses)


# pa despues porque guille dijo : (
# class GameResult(BaseModel):
#     game_word: str
#     guesses: list[str]
#     guess_result: GuessResult
#     current_streak: int


# class GameStatistics(BaseModel):
#     game_results: list[GameResult]
#     games_played: int
#     winning_percentage: int
#     max_streak: int
