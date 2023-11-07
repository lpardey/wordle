# Dependencies
import pytest
from wordle_api.schemas.game import GameState

# From apps
from wordle_api.services.game import WordleGame
from wordle_api.services.resources.schemas import GameStatus

from enum import IntEnum
class State(IntEnum):
    ONGOING_GAME = 0
    FINISHED_GAME = 1
    NO_GAME = 2



@pytest.fixture()
def basic_game_state() -> GameState:
    game_state = GameState(id=1, game_word="PIZZA", guess="CLOUD", status=GameStatus.WAITING_FOR_GUESS, result=None)
    return game_state


@pytest.fixture()
def basic_wordle_game(basic_game_state: GameState) -> WordleGame:
    wordle_game = WordleGame(game_state=basic_game_state)
    return wordle_game


@pytest.fixture()
def basic_game_storage(basic_game_state: GameState) -> GameStorage:
    game_storage = GameStorage(storage={0: basic_game_state})
    return game_storage
