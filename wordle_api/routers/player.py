# TODO: Create a statistics class. This endpoint doesn't belong here, it belongs to
# it's own endpoint which is related to the player. probably either /stats/{player_id}
# or /player/{player_id}/stats. most likely the first one.

from fastapi import APIRouter
from wordle_game.player import Player
from wordle_game.player_statistics import PlayerStatistics
from wordle_game.player_storage import PlayerStorage
from wordle_schemas.player import PlayerCreationResponse

router = APIRouter(prefix="/player", tags=["Player"])


@router.post("/")
def create_player() -> PlayerCreationResponse:
    player_storage = PlayerStorage()
    player = Player(statistics=PlayerStatistics())
    player_id = player_storage.add_player(player=player)
    return PlayerCreationResponse(player_id=player_id)


# @app.post("/player/{username}/{password}/log-in")
# def log_in() -> LogInResponse:
#     pass


# @app.post("/player/{player_id}/log-out")
# def log_out() -> LogOutResponse:
#     pass


# @app.get("/player/{player_id}/stats")
# def get_player_stats(player_id: int) -> PlayerStatisticsResponse:
#     game_state = get_game_state_by_id(game_id=game_id)
#     response = PlayerStatisticsResponse(
#         player_statistics=PlayerStatistics(
#             game_results=game_state.statistics.game_results,
#             games_played=game_state.statistics.games_played,
#             winning_percentage=game_state.statistics.winning_percentage,
#             max_streak=game_state.statistics.max_streak,
#         )
#     )
#     return response
