import pytest
from wordle_game.player import Player


@pytest.fixture()
def player() -> Player:
    return Player()
