import pytest
from wordle_game.user import User


@pytest.fixture()
def user() -> User:
    return User(user_id=0, username="guillermo", password="12345")
