from unittest import mock
from fastapi import HTTPException
import pytest
from wordle_api.game.router import create_game, get_game_status, take_a_guess
from game.game import WordleGame
from game.game_state import GameState, GameStatus, GuessResult, LetterStatus
from game.game_storage import GameStorage
from wordle_schemas.game import (
    BasicStatus,
    GameConfig,
    GameCreationResponse,
    GameStatusInfo,
    GameStatusResponse,
    TakeAGuessRequest,
)
from tests.logic_tests.conftest import basic_game_state, basic_wordle_game, basic_game_storage

#TODO: update
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


# TODO: por revisar
@pytest.mark.parametrize(
    "game_id, expected_response",
    [
        pytest.param(
            0,
            GameStatusResponse(
                status=BasicStatus.OK,
                message=None,
                game_status_info=GameStatusInfo(
                    game_word="PIZZA",
                    guesses=[],
                    game_status=GameStatus.WAITING_FOR_GUESS,
                    difficulty=0,
                    attempts_left=6,
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
                    game_word="PIZZA",
                    guesses=[],
                    game_status=GameStatus.WAITING_FOR_GUESS,
                    difficulty=0,
                    attempts_left=6,
                ),
            ),
            id="More than one game in progress",
        ),
    ],
)
@mock.patch("wordle_game.game_storage.get_game_state_by_id")
def test_get_game_status_success(
    m_get_game_state_by_id: mock.Mock,
    game_id: int,
    expected_response: GameStatusResponse,
    basic_game_state: GameState,
):
    m_get_game_state_by_id.return_value = basic_game_state
    game_storage = GameStorage()
    game_storage.storage.update({game_id: m_get_game_state_by_id.return_value})
    response = get_game_status(game_id=game_id)
    assert response == expected_response
    game_storage.storage.clear()


# TODO: por revisar
# TODO: finisht test (dunno how to)
def test_get_game_status_failure():
    with pytest.raises(HTTPException) as exc_info:
        get_game_status(game_id=7)
    assert str(exc_info.value) == ""


# TODO: por revisar
@pytest.mark.parametrize(
    "guess_request, guess_result, guess_letters_status_result, expected_response",
    [
        pytest.param(
            TakeAGuessRequest(guess="SHEEP"),
            GuessResult.NOT_GUESSED,
            [
                LetterStatus.NOT_PRESENT,
                LetterStatus.NOT_PRESENT,
                LetterStatus.NOT_PRESENT,
                LetterStatus.NOT_PRESENT,
                LetterStatus.PRESENT,
            ],
            BasicStatus.OK,
            id="Response status OK, not guessed",
        ),
        pytest.param(
            TakeAGuessRequest(guess="PIZZA"),
            GuessResult.GUESSED,
            [
                LetterStatus.IN_PLACE,
                LetterStatus.IN_PLACE,
                LetterStatus.IN_PLACE,
                LetterStatus.IN_PLACE,
                LetterStatus.IN_PLACE,
            ],
            BasicStatus.OK,
            id="Response status OK, guessed",
        ),
    ],
)
@mock.patch.object(WordleGame, "compare")
@mock.patch.object(WordleGame, "guess")
@mock.patch("wordle_game.game_storage.get_game_state_by_id")
def test_take_a_guess(
    m_get_game_state_by_id: mock.Mock,
    m_guess: mock.Mock,
    m_compare: mock.Mock,
    guess_request: TakeAGuessRequest,
    guess_result: GuessResult,
    guess_letters_status_result: list[LetterStatus],
    expected_response: BasicStatus,
    basic_game_state: GameState,
):
    m_get_game_state_by_id.return_value: GameState = basic_game_state
    m_guess.return_value = guess_result
    game_storage = GameStorage()
    game_storage.storage.update({0: m_get_game_state_by_id.return_value})
    m_compare.return_value = guess_letters_status_result

    response = take_a_guess(game_id=0, guess_request=guess_request)

    assert response.status == expected_response
    assert response.guess_result == m_guess.return_value
    assert response.guess_letters_status == m_compare.return_value

    game_storage.storage.clear()
