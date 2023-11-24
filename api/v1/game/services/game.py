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
        This function assumes guess and word are the same length.
        """
        guess = self.game_state.guess
        word = self.game_state.game_word
        letters_count = Counter(word)
        used_letters = set()  # Initialize an empty set to keep track of used letters.
        guess_letters_status = self.compare_letters(guess, word, letters_count, used_letters)
        return guess_letters_status

    def compare_letters(self, guess: str, word: str, letters_count: Counter, used_letters: set) -> list[LetterStatus]:
        """
        Compare each pair of letters in guess and word.
        """
        return [
            self.compare_letters_pair(guess_letter, word_letter, letters_count, used_letters)
            for guess_letter, word_letter in zip(guess, word)
        ]

    def compare_letters_pair(
        self, guess_letter: str, word_letter: str, letters_count: Counter, used_letters: set
    ) -> LetterStatus:
        if guess_letter == word_letter:
            return LetterStatus.IN_PLACE
        if guess_letter in letters_count and letters_count[guess_letter] > 0:
            letters_count[guess_letter] -= 1
            return self.get_present_letter_status(guess_letter, letters_count, used_letters)
        return LetterStatus.NOT_PRESENT

    def get_present_letter_status(self, guess_letter: str, letters_count: Counter, used_letters: set) -> LetterStatus:
        if guess_letter not in used_letters:
            used_letters.add(guess_letter)
            if letters_count[guess_letter] > 0:
                return LetterStatus.PRESENT_REPEATED
        return LetterStatus.PRESENT
