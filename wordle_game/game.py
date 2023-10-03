import time
from wordle_game.game_state import (
    GameResult,
    GameState,
    GameStatus,
    GuessResult,
    LetterStatus,
)
from wordle_client.game_word import AllWords


# FIVE_LETTER_WORDS: list[str] = get_words_list()


class WordleException(Exception):
    pass


class WordleGame:
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def guess(self, guess: str) -> GuessResult:
        self.validate_game_status()
        self.validate_guess(guess=guess)
        self.add_guess(guess=guess)  # If we reach this point, both the guess and the status are valid
        guess_result = self.update_game_state()
        return guess_result

    # TODO: finish and check if it's going to be used
    def new_game_countdown(self, time_in_seconds: int) -> None:
        while time_in_seconds:
            # minutes, seconds = divmod(time_in_seconds, 60)

            # if minutes > 59:
            #     hours, minutes = divmod(minutes, 60)
            # else:
            #     hours = 0

            # print(f"{hours:02d}:{minutes:02d}:{seconds:02d}", end="\r")
            time.sleep(1)
            time_in_seconds -= 1

        self.reset_game()

    # TODO: finish and check if it's going to be used
    def reset_game(self) -> None:
        # Generar una nueva partida
        #   Generar una nueva palabra
        #   Resetar los attempts a 6
        # self.game_state.status = GameStatus.WAITING_FOR_GUESS
        # self.game_state.result = GameResult.DEFEAT
        pass

    # Auxiliary functions for guess ----------------------------------------------------------------------------------

    # def add_guess_and_letter_status_result(guess: str, letter_status: list[LetterStatus]) -> list[tuple[str, list[LetterStatus]]]
    # return list(zip(guess, letter_status))

    @staticmethod
    def validate_guess(guess: str) -> None:
        if not guess.isalpha():
            raise WordleException(f"Invalid guess: At least one of the characters in '{guess}' is not alphabetic.")

        if len(guess) != 5:
            raise WordleException(f"Invalid guess: '{guess}' does not have 5 letters.")

        if guess not in AllWords.words:
            raise WordleException(f"Invalid guess: '{guess}' is not a word.")

    def validate_game_status(self) -> None:
        if self.game_state.status == GameStatus.FINISHED:
            raise WordleException("Game is over!")

    def add_guess(self, guess: str) -> None:
        guess = guess.upper()
        self.game_state.guesses.append(guess)

    def update_game_state(self) -> GuessResult:
        if self.is_victory():
            self.game_state.result = GameResult.VICTORY
            return GuessResult.GUESSED

        if self.is_defeat():
            self.game_state.result = GameResult.DEFEAT

        return GuessResult.NOT_GUESSED

    def is_victory(self) -> bool:
        if self.game_state.guesses == []:
            return False

        word = self.game_state.game_word
        guess = self.game_state.guesses[-1]
        return word == guess

    def is_defeat(self) -> bool:
        return self.game_state.guesses_left == 0

    @staticmethod
    def compare(guess: str, word: str) -> list[LetterStatus]:
        """
        This function assumes word and guess are the same length.
        """

        def _letters_comparsion(guess_letter: str, word_letter: str) -> LetterStatus | None:
            if guess_letter == word_letter:
                return LetterStatus.IN_PLACE

            if guess_letter not in letter_count:
                return LetterStatus.NOT_PRESENT

            return None

        letter_count = {letter: word.count(letter) for letter in word}
        guess_letters_status = [
            _letters_comparsion(guess_letter, word_letter) for guess_letter, word_letter in zip(guess, word)
        ]

        assigned_letters = [letter for letter, status in zip(guess, guess_letters_status) if status is not None]
        assigned_letters_count = {letter: assigned_letters.count(letter) for letter in word}

        for index, status in enumerate(guess_letters_status):
            if status is not None:
                continue
            letter = guess[index]
            if assigned_letters_count[letter] < letter_count[letter]:
                guess_letters_status[index] = LetterStatus.PRESENT
                letter_count[letter] += 1
            else:
                guess_letters_status[index] = LetterStatus.NOT_PRESENT

        return guess_letters_status
