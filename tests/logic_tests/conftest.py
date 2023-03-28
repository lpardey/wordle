import pytest
from wordle_game.game import WordleGame
from wordle_game.game_state import GameState


@pytest.fixture()
def basic_game_state():
    game_state = GameState(user_id=0, game_word="PIZZA")
    return game_state


@pytest.fixture()
def basic_wordle_game(basic_game_state: GameState):
    wordle_game = WordleGame(game_state=basic_game_state)
    return wordle_game
