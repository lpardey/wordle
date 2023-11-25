# Standard Library
from collections import Counter

# From apps
from api.v1.game.schemas.game import GameState
from api.v1.game.services.resources.game_word import AllWords
from api.v1.game.services.resources.schemas import GameStatus, GuessResult, LetterStatus, LetterStatusLiteral


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

    def compare(self) -> list[LetterStatusLiteral]:
        """
        This function assumes guess and word are the same length.
        """
        guess = self.game_state.guess
        word = self.game_state.game_word
        word_counter = Counter(word)
        guess_counter = Counter(guess)
        letter_tracker = Counter()
        result = self.get_letter_status_list(guess, word, guess_counter, word_counter, letter_tracker)
        return result

    def get_letter_status_list(
        self, guess: str, word: str, guess_counter: Counter, word_counter: Counter, letter_tracker: Counter
    ) -> list[LetterStatusLiteral]:
        return [
            self.get_letter_status(guess_letter, word_letter, guess_counter, word_counter, letter_tracker)
            for guess_letter, word_letter in zip(guess, word)
        ]

    def get_letter_status(
        self,
        guess_letter: str,
        word_letter: str,
        guess_counter: Counter,
        word_counter: Counter,
        letter_tracker: Counter,
    ) -> LetterStatusLiteral:
        if guess_letter == word_letter:
            letter_tracker[guess_letter] += 1
            return LetterStatus.IN_PLACE

        if self.is_guess_letter_present(guess_letter, word_counter, guess_counter, letter_tracker):
            return LetterStatus.PRESENT

        return LetterStatus.NOT_PRESENT

    @staticmethod
    def is_guess_letter_present(
        guess_letter: str, word_counter: Counter, guess_counter: Counter, letter_tracker: Counter
    ) -> bool:
        if guess_letter in word_counter:
            if guess_counter[guess_letter] <= word_counter[guess_letter]:
                return True

            # Update letter tracker and check if guess letter is still present in the word
            letter_tracker[guess_letter] += 1
            return letter_tracker[guess_letter] < word_counter[guess_letter]

        return False


# NAIVE V1
# def compare(self) -> list[LetterStatus]:
#     """
#     This function assumes guess and word are the same length.
#     """
#     guess = self.game_state.guess
#     word = self.game_state.game_word
#     result = []
#     letter_counter={}

#     for i in range(len(guess)):
#         if guess[i] == word[i]:
#             if guess[i] not in letter_counter:
#                 letter_counter[guess[i]] = 1
#             else:
#                 letter_counter[guess[i]] += 1
#             result.append(LetterStatus.IN_PLACE)
#         elif guess[i] in word:
#             if guess.count(guess[i]) <= word.count(guess[i]):
#                 result.append(LetterStatus.PRESENT)
#             else:
#                 if guess[i] not in letter_counter:
#                     letter_counter[guess[i]] = 1
#                 else:
#                     letter_counter[guess[i]] += 1
#                 if letter_counter[guess[i]] < word.count(guess[i]):
#                     result.append(LetterStatus.PRESENT)
#                 else:
#                     result.append(LetterStatus.PRESENT_REPEATED)
#         else:
#             result.append(LetterStatus.NOT_PRESENT)
#     return result

# NAIVE V2
# def compare(self) -> LetterStatusList:
#     """
#     This function assumes guess and word are the same length.
#     """
#     guess = self.game_state.guess
#     word = self.game_state.game_word
#     word_counter = Counter(word)
#     guess_counter = Counter(guess)
#     letter_tracker = Counter()
#     result = []

#     for guess_letter, word_letter in zip(guess, word):
#         if guess_letter == word_letter:
#             letter_tracker[guess_letter] += 1
#             result.append(LetterStatus.IN_PLACE)
#         elif guess_letter in word:
#             present_letter_status = self.get_present_letter_status(
#                 guess_letter,
#                 guess_counter,
#                 word_counter,
#                 letter_tracker,
#             )
#             result.append(present_letter_status)
#         else:
#             result.append(LetterStatus.NOT_PRESENT)

#     return result
