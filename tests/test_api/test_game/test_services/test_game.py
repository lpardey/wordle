# Dependencies
import pytest

# From apps
from api.v1.game.services.game import WordleException, WordleGame
from api.v1.game.services.resources.schemas import GameStatus, GuessResult, LetterStatus
from tests.test_api.test_game.test_services.helpers.game import compare_test_data


def test_validate_game_status_success(basic_wordle_game: WordleGame):
    try:
        basic_wordle_game.validate_game_status()
    except WordleException as e:
        assert False, f"No exception should be raised, but got {e}"


def test_validate_game_status_raises_exc(basic_wordle_game: WordleGame):
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
    "guess, expected_result",
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
def test_validate_guess_raises_exc(guess: str, expected_result: str, basic_wordle_game: WordleGame):
    basic_wordle_game.game_state.guess = guess

    with pytest.raises(WordleException) as exc:
        basic_wordle_game.validate_guess()

    assert str(exc.value) == expected_result


@pytest.mark.parametrize(
    "guess, expected_result",
    [
        pytest.param("CLOUD", GuessResult.NOT_GUESSED, id="Guess doesn't match game word"),
        pytest.param("PIZZA", GuessResult.GUESSED, id="Guess matches game word"),
    ],
)
def test_get_guess_result(expected_result: GuessResult, guess: str, basic_wordle_game: WordleGame):
    basic_wordle_game.game_state.guess = guess

    result = basic_wordle_game.get_guess_result()

    assert result == expected_result
    assert len(guess) == len(basic_wordle_game.game_state.game_word)


@pytest.mark.parametrize("guess, word, expected_result", compare_test_data())
def test_compare(guess: str, word: str, expected_result: list[LetterStatus], basic_wordle_game: WordleGame):
    basic_wordle_game.game_state.guess = guess
    basic_wordle_game.game_state.game_word = word

    result = basic_wordle_game.compare()

    assert result == expected_result
    assert len(result) == len(guess) == len(word)
