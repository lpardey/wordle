from types import NoneType
import pytest
from unittest import mock
from wordle_game.game_state import GameResult, GameState, GameStatus, GuessResult
from wordle_game.game import WordleException, WordleGame


@pytest.mark.parametrize(
    "player_guess, expected_result",
    [
        pytest.param(
            "125gu",
            "Invalid guess. At least one of the characters in '125GU' is not alphabetic.",
            id="Not alphabetic string",
        ),
        pytest.param(
            "guessing",
            "Invalid guess. 'GUESSING' does not have 5 letters.",
            id="Guess longer than 5 chars",
        ),
        pytest.param("ssgue", "Invalid guess. 'SSGUE' is not a word.", id="String is not a word"),
        pytest.param("", "Invalid guess. At least one of the characters in '' is not alphabetic.", id="Empty string"),
    ],
)
def test_validate_guess_failure(player_guess: str, expected_result: str, basic_wordle_game: WordleGame):
    with pytest.raises(WordleException) as exc_info:
        basic_wordle_game.validate_guess(guess=player_guess.upper())
    assert str(exc_info.value) == expected_result


def test_validate_guess_success(basic_wordle_game: WordleGame):
    try:
        basic_wordle_game.validate_guess(guess="SHEEP")
    except Exception as e:
        assert False, f"No exception should be raised, but got {e}"


@pytest.mark.parametrize(
    "status, expected_result",
    [pytest.param(GameStatus.FINISHED, "Game is over!", id="Invalid status. Game status is 'FINISHED'.")],
)
def test_validate_status_failure(status: GameStatus, expected_result: str):
    game_state = GameState(user_id=0, game_word="PIZZA", status=status)
    wordle = WordleGame(game_state=game_state)
    with pytest.raises(WordleException) as exc_info:
        wordle.validate_game_status()
    assert str(exc_info.value) == expected_result


def test_validate_status_success(basic_wordle_game: WordleGame):
    # la funcion validate_game_status, cuando el estado es valido, devuelve None
    # y, simplemente, NO lanza una excepcion.
    # para comprobar que esto es así, lo que tenemos que hacer es poner la invocacion
    # en un bloque try. si por cualquier cosa validate_game_status lanzase una excepcion
    # acabaríamos en el bloque except.
    # una vez ahi, sabemos que el test ha fallado y hacemos un assert False
    # para que acabe el test en error.
    # Si no se lanza ninguna excepcion durante la ejecucion de validate_game_status
    # al terminar el bloque try, pasamos de largo del except (no se ejecuta porque
    # no ha habido ninguna excepcion) y el test termina en success : )
    try:
        basic_wordle_game.validate_game_status()
    except Exception as e:
        assert False, f"No exception should be raised, but got {e}"


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


@pytest.mark.parametrize(
    "guesses, expected_result",
    [
        pytest.param([], False, id="Not victory. No guesses in game state."),
        pytest.param(["SHEEP"], False, id="Not victory. One guess in game state."),
        pytest.param(
            ["SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP"],
            False,
            id="Not victory. All possible guesses in game state.",
        ),
        pytest.param(["PIZZA"], True, id="Victory. One guess in game state."),
        pytest.param(["SHEEP", "PIZZA"], True, id="Victory. More than one guess in game state."),
        pytest.param(
            ["SHEEP", "SHEEP", "SHEEP", "SHEEP", "SHEEP", "PIZZA"],
            True,
            id="Victory. All possible guesses in game state.",
        ),
    ],
)
def test_is_victory(expected_result: bool, guesses: list[str]):
    game_state = GameState(user_id=0, game_word="PIZZA", guesses=guesses)
    wordle = WordleGame(game_state=game_state)
    result = wordle.is_victory()
    assert result == expected_result


@pytest.mark.parametrize(
    "guesses_left, expected_result",
    [
        pytest.param(0, True, id="No guesses left are a defeat"),
        pytest.param(1, False, id="Some guesses left are not a defeat"),
        pytest.param(6, False, id="All guesses left are not a defeat"),
    ],
)
@mock.patch.object(GameState, "guesses_left", new_callable=mock.PropertyMock)
def test_is_defeat(m_guesses_left: mock.Mock, basic_wordle_game: WordleGame, guesses_left: int, expected_result: bool):
    m_guesses_left.return_value = guesses_left
    result = basic_wordle_game.is_defeat()
    assert m_guesses_left.call_count == 1
    assert result == expected_result


@pytest.mark.parametrize(
    "is_victory_result, is_defeat_result, expected_status, expected_game_result, expected_result",
    [
        pytest.param(True, False, GameStatus.FINISHED, GameResult.VICTORY, GuessResult.GUESSED, id="Is victory"),
        pytest.param(False, True, GameStatus.FINISHED, GameResult.DEFEAT, GuessResult.NOT_GUESSED, id="Is defeat"),
        pytest.param(
            False,
            False,
            GameStatus.WAITING_FOR_GUESS,
            GameResult.DEFEAT,
            GuessResult.NOT_GUESSED,
            id="Neither victoy nor defeat",
        ),
        pytest.param(
            True,
            True,
            GameStatus.FINISHED,
            GameResult.VICTORY,
            GuessResult.GUESSED,
            id="Is victory but is_defeat returns 'True'",
        ),
    ],
)
@mock.patch.object(WordleGame, "is_victory")
@mock.patch.object(WordleGame, "is_defeat")
def test_update_game_state(
    m_is_defeat: mock.Mock,
    m_is_victory: mock.Mock,
    basic_wordle_game: WordleGame,
    is_victory_result: bool,
    is_defeat_result: bool,
    expected_status: GameStatus,
    expected_game_result: GameResult,
    expected_result: GuessResult,
):
    m_is_victory.return_value = is_victory_result
    m_is_defeat.return_value = is_defeat_result
    result = basic_wordle_game.update_game_state()

    assert basic_wordle_game.game_state.status == expected_status
    assert basic_wordle_game.game_state.result == expected_game_result
    assert result == expected_result
    assert m_is_victory.called
    assert not is_victory_result == m_is_defeat.called


@pytest.mark.parametrize(
    "guess, validate_guess_result, validate_game_status_result, add_guess_result, update_game_state_result, expected_result",
    [
        pytest.param(
            "PIZZA", None, None, None, GuessResult.GUESSED, GuessResult.GUESSED, id="Valid guess, player guesses"
        ),
        pytest.param(
            "SHEEP",
            None,
            None,
            None,
            GuessResult.NOT_GUESSED,
            GuessResult.NOT_GUESSED,
            id="Valid guess, player doesn't guess",
        ),
    ],
)
@mock.patch.object(WordleGame, "validate_guess")
@mock.patch.object(WordleGame, "validate_game_status")
@mock.patch.object(WordleGame, "add_guess")
@mock.patch.object(WordleGame, "update_game_state")
def test_guess(
    m_update_game_state: mock.Mock,
    m_add_guess: mock.Mock,
    m_validate_game_status: mock.Mock,
    m_validate_guess: mock.Mock,
    basic_wordle_game: WordleGame,
    guess: str,
    validate_guess_result: NoneType,
    validate_game_status_result: NoneType,
    add_guess_result: NoneType,
    update_game_state_result: GuessResult,
    expected_result: GuessResult,
):
    m_validate_guess.return_value = validate_guess_result
    m_validate_game_status.return_value = validate_game_status_result
    m_add_guess.return_value = add_guess_result
    m_update_game_state.return_value = update_game_state_result
    result = basic_wordle_game.guess(guess=guess)
    assert m_validate_guess.called
    assert m_validate_game_status.called
    assert m_add_guess.called
    assert m_update_game_state.called
    assert result == expected_result
