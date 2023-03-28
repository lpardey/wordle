from unittest import mock
from fastapi import HTTPException
import pytest
from wordle_api.game.router import create_game, get_game_state
from wordle_game.game_state import GameState, GameStatus
from wordle_game.game_storage import GameStorage
from wordle_schemas.game import BasicStatus, GameConfig, GameCreationResponse, GameStatusInfo, GameStatusResponse
from tests.logic_tests.conftest import basic_game_state, basic_wordle_game


@mock.patch.object(GameStorage, "add_game_state", return_value=0)
def test_create_game(m_add_game_state: mock.Mock):
    game_config = GameConfig()
    game_id = m_add_game_state.return_value
    result = create_game(game_config=game_config)
    expected_result = GameCreationResponse(game_id=game_id)
    assert result == expected_result
    assert m_add_game_state.call_count == 1


@mock.patch.object(GameStorage, "storage_size", return_value=0)
def test_add_game_state(m_storage_size: mock.Mock, basic_game_state: GameState):
    game_storage = GameStorage()
    result = game_storage.add_game_state(game_state=basic_game_state)
    expected_result = m_storage_size.return_value
    assert result == expected_result
    assert m_storage_size.call_count == 1


@pytest.mark.parametrize(
    "game_id, expected_response",
    [
        pytest.param(
            0,
            GameStatusResponse(
                status=BasicStatus.OK,
                message=None,
                game_status_info=GameStatusInfo(
                    game_word="PIZZA", guesses=[], game_status=GameStatus.WAITING_FOR_GUESS, difficulty=0
                ),
            ),
            id="One game in progress",
        ),
        pytest.param(
            5,
            GameStatusResponse(
                status=BasicStatus.OK,
                message=None,
                game_status_info=GameStatusInfo(
                    game_word="PIZZA", guesses=[], game_status=GameStatus.WAITING_FOR_GUESS, difficulty=0
                ),
            ),
            id="More than one game in progress",
        ),
    ],
)
@mock.patch("wordle_game.game_storage.get_game_state_by_id")
def test_get_game_state_success(
    m_get_game_state_by_id: mock.Mock,
    basic_game_state: GameState,
    game_id: int,
    expected_response: GameStatusResponse,
):
    m_get_game_state_by_id.return_value = basic_game_state
    game_storage = GameStorage()
    game_storage.storage.update({game_id: m_get_game_state_by_id.return_value})
    response = get_game_state(game_id=game_id)
    assert response == expected_response
    game_storage.storage.clear()


def test_get_game_state_failure():
    with pytest.raises(HTTPException) as exc_info:
        get_game_state(game_id=7)
    assert str(exc_info.value) == ""
