from fastapi import FastAPI, HTTPException
from wordle_schemas.game import (
    BasicStatus,
    GameCreationResponse,
    GameConfig,
    GameStatisticsResponse,
    GameStatusInfo,
    GameStatusResponse,
)
from w_game.game_state import GameState, GameStatistics, PlayerState, User

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


def get_game_state_by_id(game_id: int) -> GameState:
    game_state = GameStorage().get_game_state(index=game_id)

    if game_state is None:
        raise HTTPException(status_code=404, detail="Not found")

    return game_state


@app.get("/game/{game_id}")
def get_game_state(game_id: int) -> GameStatusResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    response = GameStatusResponse(
        game_status_info=GameStatusInfo(
            current_guess=game_state.guess,
            guess_letters=game_state.guess_letters,
            game_status=game_state.status,
        )
    )
    return response


@app.get("/game/{game_id}/stats")
def get_game_stats(game_id: int) -> GameStatisticsResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    response = GameStatisticsResponse(
        game_statistics=GameStatistics(
            game_results=game_state.statistics.game_results,
            games_played=game_state.statistics.games_played,
            winning_percentage=game_state.statistics.winning_percentage,
            max_streak=game_state.statistics.max_streak,
        )
    )
    return response


@app.post("/game")
def create_game(game_config: GameConfig) -> GameCreationResponse:
    user = User(username="guillermo", password="chachief")
    player_state = PlayerState(attempts_left=game_config.number_of_attempts, user=user)
    game_storage = GameStorage()
    game_state = GameState(player=player_state)
    game_id = game_storage.add_game_state(game_state=game_state)
    return GameCreationResponse(game_id=game_id, username=user.username)


@app.post("/game/{game_id}/guess")
def take_a_guess(game_id: int, user: User, guess_request: TakeAGuessRequest) -> TakeAGuessResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    wordle = WordleGame(game_state)
    status = BasicStatus.OK
    message = None

    if user.username != game_state.player.user.username:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        # TODO: insert wordle game function

    except WordleException as e:
        status = BasicStatus.ERROR
        message = str(e)

    response = TakeAGuessResponse(status=status, message=message)

    return response
