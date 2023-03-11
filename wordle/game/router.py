from fastapi import FastAPI
from pydantic import BaseModel
from wordle_schemas.game import GameCreationResponse, GameStatus

app = FastAPI()


class GameConfig(BaseModel):
    number_of_attempts: int = 6
    game_mode: str = "Normal"


class PlayerState(BaseModel):
    username: str
    password: str
    attempts_left: int


class GameResult(BaseModel):
    result: list


class GameState(BaseModel):
    player: PlayerState = PlayerState()
    guess: str
    game_count: int = 0
    status: GameStatus = GameStatus.AVAILABLE_TO_PLAY
    finished: bool = False
    historic_results = list[GameResult]

    def reset_guess(self) -> None:
        self.guess = "random word"


ALL_GAMES: dict[int:GameState] = {}


class GameStorage:
    def __init__(self, storage: dict[int:GameState] = ALL_GAMES) -> None:
        self.storage = storage

    def get_game_state(self, index: int) -> GameState | None:
        game_state = self.storage.get(index)
        return game_state

    def get_game_id(self, game_state: GameState) -> int:
        index_list = list(self.storage.keys())
        index = index_list.index(game_state)
        return index

    def add_game_state(self, game_state: GameState) -> None:
        index = self.storage_size()
        self.storage[index] = game_state

    def storage_size(self) -> int:
        storage_size = len(self.storage)
        return storage_size

    def reset_storage(self) -> None:
        self.storage.clear()


@app.post("/game")
def create_game(game_config: GameConfig) -> GameCreationResponse:
    player_state = PlayerState(attempts_left=game_config.number_of_attempts)
    game_state = GameState(player=player_state)
    game_state.reset_guess()
    game_storage = GameStorage()
    game_storage.add_game_state(game_state=game_state)
    game_id = game_storage.get_game_id(game_state=game_state)
    return GameCreationResponse(game={player_state.username: game_id})
