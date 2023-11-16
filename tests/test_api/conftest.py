# Standard Library
from uuid import UUID

# Dependencies
import pytest
from fastapi.testclient import TestClient

# From apps
from api.v1.game.models import Game
from api.v1.game.schemas.game import GameState
from api.v1.game.services.game import WordleGame
from api.v1.game.services.resources.schemas import GameResult, GameStatus
from api.v1.main import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


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


@pytest.fixture()
def basic_game_model() -> Game:
    game_data = {
        "id": "3c14c208-b4a0-43db-a254-95e9b3479136",
        "user": "user",
        "game_word": "pizza",
        "max_attempts": "6",
        "difficulty": "GameDifficulty.NORMAL",
        "creation_date": "A date",
        "guesses": "some guesses",
    }
    game_model = Game(**game_data)
    return game_model
