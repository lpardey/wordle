import pytest
from wordle_api.services.game import WordleGame
from game.game_state import GameState
from game.game_storage import GameStorage



@pytest.fixture()
def basic_game_state() -> GameState:
    game_state = GameState(game_word="PIZZA")
    return game_state


@pytest.fixture()
def basic_wordle_game(basic_game_state: GameState) -> WordleGame:
    wordle_game = WordleGame(game_state=basic_game_state)
    return wordle_game


@pytest.fixture()
def basic_game_storage(basic_game_state: GameState) -> GameStorage:
    game_storage = GameStorage(storage={0: basic_game_state})
    return game_storage
