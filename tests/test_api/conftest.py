# Standard Library
from typing import AsyncGenerator
from uuid import UUID

# Dependencies
import pytest
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer

# From apps
from api.v1.game.models import Game
from api.v1.game.schemas.game import GameState
from api.v1.game.services.game import WordleGame
from api.v1.game.services.resources.schemas import GameDifficulty, GameResult, GameStatus
from api.v1.main import app
from api.v1.settings import Settings, get_settings
from api.v1.user.models import User

SETTINGS = get_settings()


@pytest.fixture(scope="module")
async def test_app() -> AsyncGenerator:
    # Use an in-memory SQLite database for testing
    testing_db_url = "sqlite://:memory:"
    app.dependency_overrides[get_settings] = lambda: Settings(DATABASE_URL=testing_db_url)

    # Initializes and finalizes the Tortoise ORM for testing, specifying the models to be used and creating the in-memory database.
    initializer(SETTINGS.DATABASE_MODELS, db_url=testing_db_url, create_db=True)
    await create_records_in_db()
    yield app
    finalizer()


async def create_records_in_db() -> None:
    await create_test_user_playing_no_guesses()


async def create_test_user_playing_no_guesses() -> None:
    """User playing, no guess"""
    test_user = await User.create(username="testuser", password_hash="hashed_password")
    await Game.create(user_id=test_user.id, game_word="PIZZA", max_attempts=6, difficulty=GameDifficulty.NORMAL)


@pytest.fixture
async def test_client(test_app: AsyncGenerator) -> AsyncClient:
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def basic_game_state(
    game_id: UUID = UUID("3c14c208-b4a0-43db-a254-95e9b3479136"),
    game_word: str = "PIZZA",
    guess: str = "CLOUD",
    status: GameStatus = GameStatus.WAITING_FOR_GUESS,
    result: GameResult | None = None,
) -> GameState:
    return GameState(id=game_id, game_word=game_word, guess=guess, status=status, result=result)


@pytest.fixture()
def basic_wordle_game(basic_game_state: GameState) -> WordleGame:
    return WordleGame(game_state=basic_game_state)
