# Dependencies
import pytest
from game.player import Player


@pytest.fixture()
def player() -> Player:
    return Player()
