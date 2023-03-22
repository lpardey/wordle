from fastapi import FastAPI, HTTPException
from wordle_game.game import WordleException, WordleGame
from wordle_game.game_storage import GameStorage, get_game_state_by_id
from wordle_schemas.game import (
    BasicStatus,
    GameCreationResponse,
    GameConfig,
    GameStatusInfo,
    GameStatusResponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
)
from wordle_game.game_state import GameState, PlayerState, User

app = FastAPI()


@app.get("/game/{game_id}")
def get_game_state(game_id: int) -> GameStatusResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    response = GameStatusResponse(
        game_status_info=GameStatusInfo(
            game_word=game_state.game_word,
            current_guess=game_state.guesses[-1],
            game_status=game_state.status,
        )
    )
    return response


# TODO: Create a statistics class. This endpoint doesn't belong here, it belongs to
# it's own endpoint which is related to the user. probably either /stats/{user_id}
# or /user/{user_id}/stats. most likely the first one.
# @app.get("/game/{game_id}/stats")
# def get_game_stats(game_id: int) -> GameStatisticsResponse:
#     game_state = get_game_state_by_id(game_id=game_id)
#     response = GameStatisticsResponse(
#         game_statistics=GameStatistics(
#             game_results=game_state.statistics.game_results,
#             games_played=game_state.statistics.games_played,
#             winning_percentage=game_state.statistics.winning_percentage,
#             max_streak=game_state.statistics.max_streak,
#         )
#     )
#     return response

# TODO: Fix this function
@app.post("/game")
def create_game(game_config: GameConfig) -> GameCreationResponse:
    user = User(username="guillermo", password="chachief")
    player_state = PlayerState(attempts_left=game_config.number_of_attempts, user=user)
    game_storage = GameStorage()
    game_state = GameState(user_id=0, game_word="PIZZA")
    game_id = game_storage.add_game_state(game_state=game_state)
    return GameCreationResponse(game_id=game_id, username=user.username)


@app.post("/game/{game_id}/guess")
def take_a_guess(game_id: int, user: User, guess_request: TakeAGuessRequest) -> TakeAGuessResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    wordle = WordleGame(game_state)
    status = BasicStatus.OK
    message = None

    guess_result = None

    if user.username != game_state.player.user.username:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        guess_result = wordle.guess()

    except WordleException as e:
        status = BasicStatus.ERROR
        message = str(e)

    response = TakeAGuessResponse(status=status, message=message, guess_result=guess_result)

    return response
