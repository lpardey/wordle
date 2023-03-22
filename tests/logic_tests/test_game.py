import pytest
from unittest import mock
from wordle_game.game_state import GameState, GameStatus
from wordle_game.game import WordleException, WordleGame


@pytest.fixture
def basic_game_state():
    game_state = GameState(user_id=0, game_word="PIZZA")
    return game_state


@pytest.fixture
def basic_wordle_game(basic_game_state: GameState):
    wordle_game = WordleGame(game_state=basic_game_state)
    return wordle_game


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


@pytest.mark.parametrize(
    "status, expected_result",
    [pytest.param(GameStatus.FINISHED, "Game is over!", id="Invalid status. Game status is 'FINISHED'.")],
)
def test_validate_status_failure(expected_result: str, status: GameStatus):
    game_state = GameState(user_id=0, game_word="PIZZA", status=status)
    wordle = WordleGame(game_state=game_state)
    with pytest.raises(WordleException) as exc_info:
        wordle.validate_game_status()
    assert str(exc_info.value) == expected_result


def test_validate_status_success(basic_wordle_game: WordleGame):
    # la funcion validate_game_status, cuando el estado es valido, devuelve None
    # y, simplemente, NO lanza una excepcion.
    # para comprobar qeu esto es así, lo que tenemos que hacer es poner la invocacion
    # en un bloque try. si por cualquier cosa validate_game_status lanzase una excepcion
    # acabaríamos en el bloque except.
    # una vez ahi, sabemos que el test ha fallado y hacemos un assert False
    # para que acabe el test en error.
    # si no se lanza ninguna excepcion durante la ejecucion de validate_game_status
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
    ],
)
@mock.patch.object(GameState, "guesses_left", new_callable=mock.PropertyMock)
def test_is_defeat_by_guillermo(m_guesses_left: mock.Mock, guesses_left, expected_result: bool):
    m_guesses_left.return_value = guesses_left
    game_state = GameState(user_id=0, game_word="PIZZA")
    wordle = WordleGame(game_state=game_state)
    result = wordle.is_defeat()
    assert result == expected_result


# def update_game_state(self) -> GuessResult:
#     if self.is_victory():
#         self.game_state.status = GameStatus.FINISHED
#         self.game_state.result = GameResult.VICTORY
#         return GuessResult.GUESSED

#     if self.is_defeat():
#         self.game_state.status = GameStatus.FINISHED
#         self.game_state.result = GameResult.DEFEAT

#     return GuessResult.NOT_GUESSED
