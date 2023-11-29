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
            self.get_letter_status(
                guess, word, index, guess_letter, word_letter, guess_counter, word_counter, letter_tracker
            )
            for index, (guess_letter, word_letter) in enumerate(zip(guess, word))
        ]

    def get_letter_status(
        self,
        guess: str,
        word: str,
        index: int,
        guess_letter: str,
        word_letter: str,
        guess_counter: Counter,
        word_counter: Counter,
        letter_tracker: Counter,
    ) -> LetterStatusLiteral:
        if guess_letter == word_letter:
            letter_tracker[guess_letter] += 1
            return LetterStatus.IN_PLACE

        if self.is_guess_letter_present(guess, word, index, guess_letter, word_counter, guess_counter, letter_tracker):
            return LetterStatus.PRESENT

        return LetterStatus.NOT_PRESENT

    @staticmethod
    def is_guess_letter_present(
        guess: str,
        word: str,
        index: int,
        guess_letter: str,
        word_counter: Counter,
        guess_counter: Counter,
        letter_tracker: Counter,
    ) -> bool:
        if guess_letter in word_counter:
            if guess_counter[guess_letter] <= word_counter[guess_letter]:
                return True

            letter_tracker[guess_letter] += 1
            if letter_tracker[guess_letter] == word_counter[guess_letter] or letter_tracker[guess_letter] == len(word):
                return False
            else:
                try:
                    next_letter_index = guess.index(guess_letter, index + 1)
                except ValueError:
                    return True

            if guess[next_letter_index] == word[next_letter_index]:
                return False

            if letter_tracker[guess_letter] != guess_counter[guess_letter]:
                return False
            return True

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
#
# Naive V3
# def compare() -> list[LetterStatusLiteral]:
#     """
#     This function assumes guess and word are the same length.
#     """
#     a_g = "EMBER"
#     a_w = "FLYER"
#     b_g = "ONION"
#     b_w = "SOURS"
#     c_g = "EMBER"
#     c_w = "QUEEN"
#     d_g = "SLOTZ"
#     d_w = "COLDS"
#     guess = d_g
#     word = d_w
#     result = list(range(len(guess)))
#     index_to_letter_in_place = dict()
#     index_to_letter_present = dict()
#     final = dict()

#     # First pass: Check for correct positions
#     for i in range(len(guess)):
#         if guess[i] == word[i]:
#             index_to_letter_in_place[i] = guess[i]
#             result[i] = LetterStatus.IN_PLACE
#         elif guess[i] in word:
#             index_to_letter_present[i] = guess[i]

#     for index, letter in index_to_letter_present.items():
#         if letter in index_to_letter_in_place.values():
#             if len(index_to_letter_present) == len(index_to_letter_in_place):
#                 final.update({index: letter})
#             continue

#         if letter not in index_to_letter_in_place.values() and len(final) < len(index_to_letter_present) - 1:
#             final.update({index: letter})

#     for i in result:
#         if isinstance(i, LetterStatus):
#             continue
#         elif i in final:
#             result[i] = LetterStatus.PRESENT
#         else:
#             result[i] = LetterStatus.NOT_PRESENT

#     print(f"Letters in place: {index_to_letter_in_place}")
#     print(f"Letters present: {index_to_letter_present}")
#     print(f"Final: {final}")
#     print(f"Result: {result}")
