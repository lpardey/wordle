# Dependencies
import pytest

# From apps
from wordle_api.user.models import User
from wordle_api.user.store import UserStore, UserStoreDict


@pytest.fixture()
def basic_user() -> User:
    user = User(id=1, username="luis", password="123")
    return user