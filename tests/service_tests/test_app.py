from unittest import mock
import pytest
from wordle.game.router import GameConfig, GameStorage, create_game

def test_create_first_game():
    game_storage = GameStorage()
    assert game_storage.storage_size() == 0
    game_config = GameConfig()
    response = create_game(game_config=game_config)
    game_state = response.game.get(0)
    assert game_storage.get_game_id(game_state=game_state) == 0
    assert game_storage.storage_size() == 1


# @app.post("/game")
# def create_game(game_config: GameConfig) -> GameCreationResponse:
#     player_state = PlayerState(attempts_left=game_config.number_of_attempts)
#     game_state = GameState(player=player_state)
#     game_state.reset_guess()
#     game_storage = GameStorage()
#     game_storage.add_game_state(game_state=game_state)
#     game_id = game_storage.get_game_id(game_state=game_state)
#     return GameCreationResponse(game={player_state.username: game_id})
