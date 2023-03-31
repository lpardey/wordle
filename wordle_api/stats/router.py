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