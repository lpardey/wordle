from unittest import mock, TestCase
from wordle_api.game.router import create_game
from wordle_game.game_state import GameState
from wordle_game.game_storage import GameStorage
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
    @mock.patch.object(GameStorage, "add_game_state", return_value=0)
    def test_create_game(self, m_add_game_state: mock.Mock):
        game_config = GameConfig()
        game_id = m_add_game_state.return_value
        game_username = "guillermo"
        result = create_game(game_config=game_config)
        expected_result = GameCreationResponse(game_id=game_id, username=game_username)
        self.assertEqual(result, expected_result)
        assert m_add_game_state.assert_called

    @mock.patch.object(GameStorage, "storage_size", return_value=0)
    def test_add_game_state(self, m_storage_size: mock.Mock):
        game_storage = GameStorage()
        game_state = GameState(user_id=0, game_word="PIZZA")
        result = game_storage.add_game_state(game_state=game_state)
        expected_result = m_storage_size.return_value
        self.assertEqual(result, expected_result)
        assert m_storage_size.assert_called


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


# @mock.patch.object(GameStorage, "get_game_state", return_value=GameState())
# def test_get_game_stats(m_get_game_state: mock.Mock):
#     game_state: GameState = m_get_game_state.return_value
#     game_id = 0
#     response = get_game_stats(game_id=game_id)
#     assert m_get_game_state.assert_called_once
#     assert m_get_game_state.call_args_list[0][1]["index"] == game_id
#     assert m_get_game_state.call_args == mock.call(index=game_id)
#     assert response.game_statistics.game_results == game_state.statistics.game_results
#     assert response.game_statistics.games_played == game_state.statistics.games_played
#     assert response.game_statistics.winning_percentage == game_state.statistics.winning_percentage
#     assert response.game_statistics.max_streak == game_state.statistics.max_streak


# @pytest.mark.parametrize(
#     "guess_request, expected_status",
#     [
#         pytest.param(TakeAGuessRequest(guess="pizza"), BasicStatus.OK, id="Valid guess, player guesses."),
#         pytest.param(TakeAGuessRequest(guess="sheep"), BasicStatus.OK, id="Valid guessing, player doesn't guess."),
#         pytest.param(
#             TakeAGuessRequest(guess="125guess"), BasicStatus.ERROR, id="Invalid guess, not alphabetic string"
#         ),
#         pytest.param(
#             TakeAGuessRequest(guess="guessing"), BasicStatus.ERROR, id="Invalid guess, string doesn't have 5 letters"
#         ),
#         pytest.param(TakeAGuessRequest(guess="ssgue"), BasicStatus.ERROR, id="Invalid guess, string is not a word"),
#         pytest.param(TakeAGuessRequest(guess=""), BasicStatus.ERROR, id="Invalid guess, empty string"),
#     ],
# )
# @mock.patch.object(GameStorage, "get_game_state", return_value=GameState())
# @mock.patch.object(WordleGame, "place_guess", return_value=None)
# @mock.patch.object(WordleGame, "compare_words")
# @mock.patch.object(WordleGame, "get_guess_result")
# def test_take_a_guess_ok_result(
#     m_get_guess_result: mock.Mock,
#     m_compare_words: mock.Mock,
#     m_place_guess: mock.Mock,
#     m_get_game_state: mock.Mock,
#     guess_request: TakeAGuessRequest,
#     expected_status: BasicStatus,
#     user: User,
# ):
#     game_id = 0
#     game_state: GameState = m_get_game_state.return_value
#     wordle = WordleGame(game_state=game_state)
#     response = take_a_guess(game_id=game_id, user=user, guess_request=guess_request)
#     assert user.username == game_state.player.user.username
#     assert response.status == expected_status
#     if response.status.OK:
#         m_get_guess_result.return_value = GuessResult(
#             player_guess=game_state.player.player_guess,
#             letters_available=game_state.letters_available,
#             letters_in_place=game_state.letters_in_place,
#             letters_out_of_place=game_state.letters_out_of_place,
#             letters_not_in_word=game_state.letters_not_in_word,
#             guess_result=GuessResultEnum.GUESSED,
#         )
#         m_compare_words.return_value = {0: {"P": True}, 1: {"I": True}, 2: {"Z": True}, 3: {"Z": True}, 4: {"A": True}}
#         assert wordle.compare_words() == m_compare_words.return_value
#         assert response.guess_result == m_get_guess_result.return_value
#         m_get_guess_result.return_value = GuessResult(
#             player_guess=game_state.player.player_guess,
#             letters_available=game_state.letters_available,
#             letters_in_place=game_state.letters_in_place,
#             letters_out_of_place=game_state.letters_out_of_place,
#             letters_not_in_word=game_state.letters_not_in_word,
#             guess_result=GuessResultEnum.NOT_GUESSED,
#         )
#         m_compare_words.return_value = {4: {"P": False}}
#         assert wordle.compare_words() == m_compare_words.return_value
#         assert response.guess_result == m_get_guess_result.return_value
#         m_place_guess.assert_called
#         m_compare_words.assert_called
#         m_get_guess_result.assert_called
