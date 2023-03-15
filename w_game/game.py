from enum import Enum
from pydantic import BaseModel

# schema = transferir informacion --- esto va en la API
# modelo = almacenar informacion --- esto va en la base de datos


class User(BaseModel):
    username: str
    password: str


class PlayerState(BaseModel):
    attempts_left: int


class GameResult(BaseModel):
    result: list


class Guess(BaseModel):
    guess: str


class WordleLetters(BaseModel):
    letters_in_place: list[str]
    letters_out_of_place: list[str]
    letters_not_in_word: list[str]
    letters_available: list[str]


class GameStatus(str, Enum):
    AVAILABLE_TO_PLAY = "AVAILABLE_TO_PLAY"
    WAITING_FOR_GUESS = "WAITING_FOR_GUESS"
    NOT_AVAILABLE_TO_PLAY = "NOT_AVAILABLE_TO_PLAY"


class GameState(BaseModel):
    player: PlayerState = PlayerState(attempts_left=6)
    game_word: str = "random word"
    guess: Guess = Guess(guess="Guess")
    guess_letters: WordleLetters = WordleLetters(
        letters_in_place=[],
        letters_out_of_place=[],
        letters_not_in_word=[],
        letters_available=[],
    )
    status: GameStatus = GameStatus.AVAILABLE_TO_PLAY
    finished: bool = False


class UserHistory(BaseModel):
    game_count: int = 0
    historic_results: list[GameResult] = []
