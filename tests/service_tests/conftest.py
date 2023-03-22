import pytest
from wordle_game.game_state import User


@pytest.fixture
def user() -> User:
    return User(username="user", password="12345")
