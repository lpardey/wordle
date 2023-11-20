# Standard Library
from collections import Counter

# From apps
from api.v1.game.schemas.game import GameState
from api.v1.game.services.resources.game_word import AllWords
from api.v1.game.services.resources.schemas import GameStatus, GuessResult, LetterStatus


class WordleException(Exception):
    pass


class WordleGame:
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def guess(self) -> GuessResult:
        self.validate_game_status()
        self.validate_guess()
        guess_result = self.get_guess_result()
        return guess_result

    def validate_game_status(self) -> None:
        if self.game_state.status == GameStatus.FINISHED:
            raise WordleException("Game is over!")

    def validate_guess(self) -> None:
        guess = self.game_state.guess
        if not guess.isalpha():
            message = (
                "Guess cannot be empty!"
                if guess == ""
                else f"Invalid guess: At least one of the characters in '{guess}' is not alphabetic."
            )
            raise WordleException(message)
        if len(guess) != 5:
            raise WordleException(f"Invalid guess: '{guess}' does not have 5 letters.")
        if guess not in AllWords.words:
            raise WordleException(f"Invalid guess: '{guess}' is not a word.")

    def get_guess_result(self) -> GuessResult:
        if self.game_state.game_word == self.game_state.guess:
            return GuessResult.GUESSED
        return GuessResult.NOT_GUESSED

    def compare(self) -> list[LetterStatus]:
        """
        This function assumes word and guess are the same length.
        """

        def _compare_letters(guess_letter: str, word_letter: str) -> LetterStatus:
            if guess_letter == word_letter:
                return LetterStatus.IN_PLACE
            if guess_letter in letter_count and letter_count[guess_letter] > 0:
                letter_count[guess_letter] -= 1
                return LetterStatus.PRESENT
            return LetterStatus.NOT_PRESENT

        guess = self.game_state.guess
        word = self.game_state.game_word
        letter_count = Counter(word)
        guess_letters_status = [
            _compare_letters(guess_letter, word_letter) for guess_letter, word_letter in zip(guess, word)
        ]
        return guess_letters_status
