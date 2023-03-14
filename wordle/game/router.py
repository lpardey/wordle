from fastapi import FastAPI
from wordle_schemas.game import GameCreationResponse, GameConfig
from w_game.game import GameState, PlayerState, User


app = FastAPI()

ALL_GAMES: dict[int:GameState] = {}


class GameStorage:
    def __init__(self, storage: dict[int:GameState] = ALL_GAMES) -> None:
        self.storage = storage

    def get_game_state(self, index: int) -> GameState | None:
        game_state = self.storage.get(index)
        return game_state

    def get_game_id(self, game_state: GameState) -> int | None:
        for key, game in self.storage.items():
            if game == game_state:
                return key

    def add_game_state(self, game_state: GameState) -> int:
        index = self.storage_size()
        self.storage[index] = game_state
        return index

    def storage_size(self) -> int:
        storage_size = len(self.storage)
        return storage_size

    def reset_storage(self) -> None:
        self.storage.clear()


@app.post("/game")
def create_game(game_config: GameConfig) -> GameCreationResponse:
    player_state = PlayerState(attempts_left=game_config.number_of_attempts)
    game_state = GameState(player=player_state, guess="random word")
    game_state.reset_guess()
    user = User(username="guillermo", password="chachief")
    game_storage = GameStorage()
    game_id = game_storage.add_game_state(game_state=game_state)
    return GameCreationResponse(game_id=game_id, username=user.username)




