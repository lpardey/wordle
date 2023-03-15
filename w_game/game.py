from enum import Enum
from pydantic import BaseModel

# schema = transferir informacion --- esto va en la API
# modelo = almacenar informacion --- esto va en la base de datos


class User(BaseModel):
    username: str
    password: str


class PlayerState(BaseModel):
    attempts_left: int
    user: User


class GameResultEnum(str, Enum):
    GUESSED = "GUESSED"
    NOT_GUESSED = "NOT_GUESSED"


class Guess(BaseModel):
    guess: str


class WordleLetters(BaseModel):
    letters_in_place: list[str]
    letters_out_of_place: list[str]
    letters_not_in_word: list[str]
    letters_available: list[str]


class GuessResult(BaseModel):
    player_guess: Guess
    game_letters: WordleLetters
    game_result: GameResultEnum
    current_streak: int


class GameStatistics(BaseModel):
    game_results: list[GuessResult]
    games_played: int
    winning_percentage: int
    max_streak: int


class GameStatus(str, Enum):
    AVAILABLE_TO_PLAY = "AVAILABLE_TO_PLAY"
    WAITING_FOR_GUESS = "WAITING_FOR_GUESS"
    NOT_AVAILABLE_TO_PLAY = "NOT_AVAILABLE_TO_PLAY"


class GameState(BaseModel):
    player: PlayerState = PlayerState(attempts_left=6, user=User(username="guillermo", password="12345"))
    game_word: str = "random word"
    guess: Guess = Guess(guess="Guess")
    guess_letters: WordleLetters = WordleLetters(
        letters_in_place=[],
        letters_out_of_place=[],
        letters_not_in_word=[],
        letters_available=[],
    )
    status: GameStatus = GameStatus.AVAILABLE_TO_PLAY
    statistics: GameStatistics = GameStatistics(
        game_results=[
            GuessResult(
                player_guess=Guess(guess="random word"),
                game_letters=WordleLetters(
                    letters_in_place=[],
                    letters_out_of_place=[],
                    letters_not_in_word=[],
                    letters_available=[],
                ),
                game_result=GameResultEnum.GUESSED,
                current_streak=1,
            )
        ],
        games_played=1,
        winning_percentage=100,
        max_streak=1,
    )
    finished: bool = False
