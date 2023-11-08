# Standard Library
from enum import IntEnum

# Dependencies
import pytest

# From apps
from api.schemas.game import GameState
from api.services.game import WordleGame
from api.services.resources.schemas import GameResult, GameStatus


class State(IntEnum):
    ONGOING_GAME = 0
    FINISHED_GAME = 1


@pytest.fixture()
def basic_game_state(state: State) -> GameState:
    if state == State.ONGOING_GAME:
        game_state = GameState(
            id=1,
            game_word="PIZZA",
            guess="CLOUD",
            status=GameStatus.WAITING_FOR_GUESS,
            result=None,
        )
    else:
        game_state = GameState(
            id=1,
            game_word="PIZZA",
            guess="PIZZA",
            status=GameStatus.FINISHED,
            result=GameResult.VICTORY,
        )
    return game_state


@pytest.fixture()
def basic_wordle_game(basic_game_state: GameState) -> WordleGame:
    wordle_game = WordleGame(game_state=basic_game_state)
    return wordle_game


@pytest.fixture()
def basic_game_storage(basic_game_state: GameState) -> GameStorage:
    game_storage = GameStorage(storage={0: basic_game_state})
    return game_storage
