from unittest import mock, TestCase
import pytest
from w_game.game import GameState, PlayerState, User
from wordle.game.router import GameStorage, create_game
from wordle_schemas.game import GameConfig, GameCreationResponse


# def test_create_game():
#     game_storage = GameStorage()
#     assert game_storage.storage_size() == 0

#     game_config = GameConfig()
#     response = create_game(game_config=game_config)
#     game_id = response.game_id
#     game_state = game_storage.get_game_state(index=game_id)

#     assert game_storage.get_game_id(game_state=game_state) == game_id
#     assert game_storage.storage_size() == 1

#     game_storage.reset_storage()


# @pytest.fixture
# def base_game_config() -> GameConfig:
#     return GameConfig()


# # @mock.patch.object(GameStorage, "storage_size", return_value=1)
# # @mock.patch.object(GameStorage, "get_game_id", return_value=0)
# # def test_create_game2(m_get_game_id: mock.Mock, m_storage_size: mock.Mock):
# #     storage = GameStorage()
# #     assert len(storage.storage) == 0

# #     game_config = GameConfig()
# #     response = create_game(game_config=game_config)
# #     assert m_storage_size.assert_called_once
# #     game_id = m_get_game_id.return_value
# #     assert game_id == response.game_id

# #     storage_size = m_storage_size.return_value
# #     assert storage_size == len(storage.storage)

# #     storage.reset_storage()

# @mock.patch("wordle.game.router.GameStorage.storage_size", return_value = 1)
# @mock.patch("wordle.game.router.GameStorage.get_game_id", return_value = 0)
# def test_create_game3(m_get_game_id: mock.Mock, m_storage_size: mock.Mock):
#     storage = GameStorage()
#     storage.reset_storage()
#     assert len(storage.storage) == 0

#     game_config = GameConfig()
#     response = create_game(game_config=game_config)
#     assert m_storage_size.assert_called_once
#     assert m_get_game_id.return_value == response.game_id
#     assert m_storage_size.return_value == len(storage.storage)

#     storage.reset_storage()

# @mock.patch("wordle.game.router.GameStorage.add_game_state", return_value = 0)
# def test_create_game2(m_add_game_state: mock.Mock):
#     game_storage = GameStorage()
#     assert len(game_storage.storage) == 0

#     user = User(username="guillermo", password="chachief")
#     game_config = GameConfig()

#     game_id = m_add_game_state.return_value
#     game_username = user.username
#     response = create_game(game_config=game_config)

#     assert response.game_id == game_id
#     assert response.username == game_username

#     game_storage.reset_storage()


# @mock.patch("wordle.game.router.GameStorage.add_game_state", return_value = 0)
# @mock.patch("w_game.game.GameState.reset_guess", return_value = None)
# def test_create_game5(m_reset_guess: mock.Mock, m_add_game_state: mock.Mock):
#     game_storage = GameStorage()
#     assert len(game_storage.storage) == 0

#     user = User(username="guillermo", password="chachief")
#     game_config = GameConfig()
#     game_guess = m_reset_guess.return_value
#     game_id = m_add_game_state.return_value
#     game_username = user.username
#     response = create_game(game_config=game_config)
#     assert len(game_storage.storage) == 1
#     response_game_state: GameState = game_storage.storage.get(response.game_id)

#     assert response.game_id == game_id
#     assert response.username == game_username
#     assert response_game_state.guess == game_guess

#     game_storage.reset_storage()


class TestCreateGame(TestCase):
    @mock.patch("wordle.game.router.GameStorage.add_game_state", return_value=0)
    def test_create_game(self, m_add_game_state: mock.Mock):
        game_config = GameConfig()
        game_id = m_add_game_state.return_value
        game_username = "guillermo"
        result = create_game(game_config=game_config)
        expected_result = GameCreationResponse(game_id=game_id, username=game_username)
        self.assertEqual(result, expected_result)
        assert m_add_game_state.assert_called

    @mock.patch("wordle.game.router.GameStorage.storage_size", return_value=0)
    def test_add_game_state(self, m_storage_size: mock.Mock):
        game_storage = GameStorage()
        game_state = GameState(guess="random word")
        result = game_storage.add_game_state(game_state=game_state)
        expected_result = m_storage_size.return_value
        self.assertEqual(result, expected_result)
        assert m_storage_size.assert_called


