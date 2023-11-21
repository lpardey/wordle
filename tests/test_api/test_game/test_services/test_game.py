# Standard Library
from unittest.mock import Mock, PropertyMock, patch

# Dependencies
import pytest

# From apps
from api.v1.game.schemas.game import GameState
from api.v1.game.services.game import WordleException, WordleGame
from api.v1.game.services.resources.schemas import GameResult, GameStatus, GuessResult


def test_validate_game_status_success(basic_wordle_game: WordleGame):
    try:
        basic_wordle_game.validate_game_status()
    except WordleException as e:
        assert False, f"No exception should be raised, but got {e}"


def test_validate_status_failure(basic_wordle_game: WordleGame):
    basic_wordle_game.game_state.status = GameStatus.FINISHED
    with pytest.raises(WordleException) as exc_info:
        basic_wordle_game.validate_game_status()
    assert str(exc_info.value) == "Game is over!"


def test_validate_guess_success(basic_wordle_game: WordleGame):
    try:
        basic_wordle_game.validate_guess()
    except WordleException as exc:
        assert False, f"No exception should be raised, but got: {exc}"


@pytest.mark.parametrize(
    "player_guess, expected_result",
    [
        pytest.param(
            "125GU",
            "Invalid guess: At least one of the characters in '125GU' is not alphabetic.",
            id="Guess is not an alphabetic string",
        ),
        pytest.param(
            "GUESSING",
            "Invalid guess: 'GUESSING' does not have 5 letters.",
            id="Guess is longer than 5 characters",
        ),
        pytest.param("SSGUE", "Invalid guess: 'SSGUE' is not a word.", id="Guess is not a word"),
        pytest.param("", "Guess cannot be empty!", id="Guess is empty"),
    ],
)
def test_validate_guess_failure(player_guess: str, expected_result: str, basic_wordle_game: WordleGame):
    basic_wordle_game.game_state.guess = player_guess
    with pytest.raises(WordleException) as exc:
        basic_wordle_game.validate_guess()
    assert str(exc.value) == expected_result


@pytest.mark.parametrize(
    "player_guess, expected_result",
    [
        pytest.param("CLOUD", GuessResult.NOT_GUESSED, id="Guess doesn't match game word"),
        pytest.param("PIZZA", GuessResult.GUESSED, id="Guess matches game word"),
    ],
)
def test_get_guess_result(expected_result: GuessResult, player_guess: str, basic_wordle_game: WordleGame):
    basic_wordle_game.game_state.guess = player_guess
    guess_result = basic_wordle_game.get_guess_result()
    assert guess_result == expected_result


@pytest.mark.skip("Work in progress")
@pytest.mark.parametrize(
    "guess, guesses, expected_result",
    [
        pytest.param("sheep", [], ["SHEEP"], id="First guess."),
        pytest.param("cloud", ["SHEEP"], ["SHEEP", "CLOUD"], id="One or more guesses in game state."),
        pytest.param(
            "cloud",
            ["SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP"],
            ["SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP", "CLOUD"],
            id="All possible guesses in game state.",
        ),
    ],
)
def test_add_guess(expected_result: list[str], guesses: list[str], guess: str, basic_wordle_game: WordleGame):
    basic_wordle_game.game_state.guesses = guesses
    basic_wordle_game.add_guess(guess=guess)
    assert basic_wordle_game.game_state.guesses == expected_result


# @pytest.mark.parametrize(
#     "guesses, expected_result",
#     [
#         pytest.param([], False, id="Not victory. No guesses in game state."),
#         pytest.param(["SHEEP"], False, id="Not victory. One guess in game state."),
#         pytest.param(
#             ["SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP"],
#             False,
#             id="Not victory. All possible guesses in game state.",
#         ),
#         pytest.param(["PIZZA"], True, id="Victory. One guess in game state."),
#         pytest.param(["SHEEP", "PIZZA"], True, id="Victory. More than one guess in game state."),
#         pytest.param(
#             ["SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP", "PIZZA"],
#             True,
#             id="Victory. All possible guesses in game state.",
#         ),
#     ],
# )
# def test_is_victory(expected_result: bool, guesses: list[str]):
#     game_state = GameState(player=Player(statistics=PlayerStatistics()), game_word="PIZZA", guesses=guesses)
#     wordle = WordleGame(game_state=game_state)
#     result = wordle.is_victory()
#     assert result == expected_result


@pytest.mark.skip("Work in progress")
@pytest.mark.parametrize(
    "guesses_left, expected_result",
    [
        pytest.param(0, True, id="No guesses left are a defeat"),
        pytest.param(1, False, id="Some guesses left are not a defeat"),
        pytest.param(6, False, id="All guesses left are not a defeat"),
    ],
)
@patch.object(GameState, "guesses_left", new_callable=PropertyMock)
def test_is_defeat(m_guesses_left: Mock, basic_wordle_game: WordleGame, guesses_left: int, expected_result: bool):
    m_guesses_left.return_value = guesses_left
    result = basic_wordle_game.is_defeat()
    assert m_guesses_left.call_count == 1
    assert result == expected_result


@pytest.mark.skip("Work in progress")
@pytest.mark.parametrize(
    "is_victory_result, is_defeat_result, expected_game_result, expected_guess_result",
    [
        pytest.param(True, False, GameResult.VICTORY, GuessResult.GUESSED, id="Is victory"),
        pytest.param(False, True, GameResult.DEFEAT, GuessResult.NOT_GUESSED, id="Is defeat"),
        pytest.param(
            False,
            False,
            GameResult.DEFEAT,
            GuessResult.NOT_GUESSED,
            id="Neither victoy nor defeat",
        ),
        pytest.param(
            True,
            True,
            GameResult.VICTORY,
            GuessResult.GUESSED,
            id="Is victory but is_defeat returns 'True'",
        ),
    ],
)
@patch.object(WordleGame, "is_victory")
@patch.object(WordleGame, "is_defeat")
def test_update_game_state(
    m_is_defeat: Mock,
    m_is_victory: Mock,
    basic_wordle_game: WordleGame,
    is_victory_result: bool,
    is_defeat_result: bool,
    expected_game_result: GameResult,
    expected_guess_result: GuessResult,
):
    m_is_victory.return_value = is_victory_result
    m_is_defeat.return_value = is_defeat_result

    guess_result = basic_wordle_game.update_game_state()

    assert basic_wordle_game.game_state.result == expected_game_result
    assert guess_result == expected_guess_result
    assert m_is_victory.called
    assert is_victory_result != m_is_defeat.called


@pytest.mark.skip("Work in progress")
@pytest.mark.parametrize(
    "guess, update_game_state_result, expected_guess_result",
    [
        pytest.param("PIZZA", GuessResult.GUESSED, GuessResult.GUESSED, id="Player guesses"),
        pytest.param("SHEEP", GuessResult.NOT_GUESSED, GuessResult.NOT_GUESSED, id="Player doesn't guess"),
    ],
)
@patch.object(WordleGame, "validate_guess", return_value=None)
@patch.object(WordleGame, "validate_game_status", return_value=None)
@patch.object(WordleGame, "add_guess", return_value=None)
@patch.object(WordleGame, "update_game_state")
def test_guess_success(
    m_update_game_state: Mock,
    m_add_guess: Mock,
    m_validate_game_status: Mock,
    m_validate_guess: Mock,
    guess: str,
    update_game_state_result: GuessResult,
    expected_guess_result: GuessResult,
    basic_wordle_game: WordleGame,
):
    m_update_game_state.return_value = update_game_state_result

    result = basic_wordle_game.guess(guess=guess)

    assert m_validate_guess.call_count == 1
    assert m_validate_guess.call_args_list[0][1]["guess"] == guess

    assert m_validate_game_status.call_count == 1

    assert m_add_guess.call_count == 1
    assert m_add_guess.call_args_list[0][1]["guess"] == guess

    assert m_update_game_state.call_count == 1

    assert result == expected_guess_result


@pytest.mark.skip("Work in progress")
@pytest.mark.parametrize(
    "guess, game_status, validate_guess_side_effect, validate_game_status_side_effect",
    [
        pytest.param(
            "7SHEP",
            GameStatus.WAITING_FOR_GUESS,
            WordleException("Invalid guess. At least one of the characters in '7SHEP' is not alphabetic."),
            None,
            id="guess is not alphabetic",
        ),
        pytest.param(
            "SHEEPY",
            GameStatus.WAITING_FOR_GUESS,
            WordleException("Invalid guess. 'SHEEPY' does not have 5 letters."),
            None,
            id="Guess doesn't have 5 letters",
        ),
        pytest.param(
            "NOWOR",
            GameStatus.WAITING_FOR_GUESS,
            WordleException("Invalid guess. 'NOWOR' is not a word."),
            None,
            id="Guess is not a word",
        ),
        pytest.param("SHEEP", GameStatus.FINISHED, None, WordleException("Game is over!"), id="Game is finished"),
    ],
)
@patch.object(GameState, "status", new_callable=PropertyMock)
def test_guess_failure(
    m_game_state_status: Mock,
    guess: str,
    game_status: GameStatus,
    validate_guess_side_effect: WordleException | None,
    validate_game_status_side_effect: WordleException | None,
    basic_wordle_game: WordleGame,
):
    m_game_state_status.return_value = game_status
    first_side_effect = validate_guess_side_effect or validate_game_status_side_effect
    expected_message = str(first_side_effect)

    with pytest.raises(WordleException) as exc_info:
        basic_wordle_game.guess(guess=guess)

    assert str(exc_info.value) == expected_message
