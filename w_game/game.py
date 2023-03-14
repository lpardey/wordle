from pydantic import BaseModel
from wordle_schemas.game import GameStatus

# schema = transferir informacion --- esto va en la API
# modelo = almacenar informacion --- esto va en la base de datos


class User(BaseModel):
    username: str
    password: str


class PlayerState(BaseModel):
    attempts_left: int


class GameResult(BaseModel):
    result: list


class GameState(BaseModel):
    player: PlayerState = PlayerState(attempts_left=6)
    guess: str
    status: GameStatus = GameStatus.AVAILABLE_TO_PLAY
    finished: bool = False

    def reset_guess(self) -> None:
        self.guess = "random word"


class UserHistory(BaseModel):
    game_count: int = 0
    historic_results: list[GameResult] = []
