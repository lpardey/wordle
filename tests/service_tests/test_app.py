from unittest import mock, TestCase
from fastapi import HTTPException
import fastapi

import pytest
from wordle_api.game.router import create_game, get_game_state
from wordle_game.game_state import GameState, GameStatus, User
from wordle_game.game_storage import GameStorage
from wordle_schemas.game import BasicStatus, GameConfig, GameCreationResponse, GameStatusInfo, GameStatusResponse


class TestCreateGame(TestCase):
    @mock.patch.object(GameStorage, "add_game_state", return_value=0)
    def test_create_game(self, m_add_game_state: mock.Mock):
        game_config = GameConfig()
        user = User()
        game_id = m_add_game_state.return_value
        result = create_game(game_config=game_config)
        expected_result = GameCreationResponse(game_id=game_id, username=user.username)
        self.assertEqual(result, expected_result)
        m_add_game_state.assert_called()

    @mock.patch.object(GameStorage, "storage_size", return_value=0)
    def test_add_game_state(self, m_storage_size: mock.Mock):
        game_storage = GameStorage()
        game_state = GameState(user_id=0, game_word="PIZZA")
        result = game_storage.add_game_state(game_state=game_state)
        expected_result = m_storage_size.return_value
        self.assertEqual(result, expected_result)
        m_storage_size.assert_called()


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
@mock.patch("wordle_game.game_storage.get_game_state_by_id", return_value=GameState(user_id=0, game_word="PIZZA"))
def test_get_game_state_success(
    m_get_game_state_by_id: mock.Mock,
    game_id: int,
    expected_response: GameStatusResponse,
):
    game_state = m_get_game_state_by_id.return_value
    GameStorage().storage.update({game_id: game_state})
    response = get_game_state(game_id=game_id)
    assert response == expected_response


def test_get_game_state_failure():
    GameStorage().storage = {}

    with pytest.raises(HTTPException) as exc_info:
        get_game_state(game_id=7)
    assert str(exc_info.value) == ""


# @app.get("/game/{game_id}")
# def get_game_state(game_id: int) -> GameStatusResponse:
#     game_state = get_game_state_by_id(game_id=game_id)
#     response = GameStatusResponse(
#         game_status_info=GameStatusInfo(
#             game_word=game_state.game_word,
#             guesses=game_state.guesses,
#             game_status=game_state.status,
#             difficulty=game_state.difficulty,
#         )
#     )
#     return response


# @mock.patch.object(GameStorage, "get_game_state", return_value=GameState())
# def test_get_game_state(m_get_game_state: mock.Mock):
#     game_state: GameState = m_get_game_state.return_value
#     game_id = 0
#     response = get_game_state(game_id=game_id)
#     assert m_get_game_state.assert_called_once
#     assert m_get_game_state.call_args_list[0][1]["index"] == game_id
#     assert response.message is None
#     assert response.status == BasicStatus.OK
#     assert response.game_status_info.current_guess == game_state.player.player_guess
#     assert response.game_status_info.letters_available == game_state.letters_available
#     assert response.game_status_info.letters_in_place == game_state.letters_in_place
#     assert response.game_status_info.letters_out_of_place == game_state.letters_out_of_place
#     assert response.game_status_info.letters_not_in_word == game_state.letters_not_in_word
#     assert response.game_status_info.game_status == game_state.status
