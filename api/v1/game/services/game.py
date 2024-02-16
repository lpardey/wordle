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
        guess = self.game_state.guess
        word = self.game_state.game_word
        result = [None] * len(guess)
        remaining_letters = {letter: word.count(letter) for letter in word}

        # First evaluation: marks letters in place and not present
        for i in range(len(guess)):
            if guess[i] == word[i]:
                result[i] = LetterStatus.IN_PLACE
                remaining_letters[guess[i]] -= 1
            elif guess[i] not in remaining_letters:
                result[i] = LetterStatus.NOT_PRESENT

        # Second evaluation: marks letters present
        for i in range(len(guess)):
            if result[i] == None:
                if remaining_letters[guess[i]] > 0:
                    result[i] = LetterStatus.PRESENT
                    remaining_letters[guess[i]] -= 1
                else:
                    result[i] = LetterStatus.NOT_PRESENT

        return result
