import pytest
from wordle_game.game_state import GameState
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
def test_validate_guess(player_guess: str, expected_result: str):
    game_state = GameState(user_id=0, game_word="PIZZA")
    wordle_game = WordleGame(game_state=game_state)
    with pytest.raises(WordleException) as exc_info:
        wordle_game.validate_guess(guess=player_guess.upper())
    assert str(exc_info.value) == expected_result


    # def validate_guess(guess: str) -> None:
    #     if not guess.isalpha():
    #         raise WordleException(f"Invalid guess. At least one of the characters in '{guess}' is not alphabetic.")

    #     if len(guess) != 5:
    #         raise WordleException(f"Invalid guess. '{guess}' does not have 5 letters.")

    #     if guess not in FIVE_LETTER_WORDS:
    #         raise WordleException(f"Invalid guess. '{guess}' is not a word.")

    # def validate_game_status(self) -> None:
    #     if self.game_state.status == GameStatus.FINISHED:
    #         raise WordleException(f"Game is over!")

    # def add_guess(self, guess: str) -> None:
    #     guess = guess.upper()
    #     self.game_state.guesses.append(guess)
