# From apps
from wordle_api.models import Game, Guess
from wordle_api.services.resources.schemas import GameResult, GameStatus, GuessResult, LetterStatus
from wordle_client.game_word import AllWords


class WordleException(Exception):
    pass


class WordleGame:
    def __init__(self, game: Game) -> None:
        self.game = game

    async def guess(self, guess: str) -> GuessResult:
        await self.validate_game_status()
        self.validate_guess(guess)
        await Guess.create(game_id=self.game.id, value=guess)
        guess_result = await self.get_guess_result()
        return guess_result

    @staticmethod
    def validate_guess(guess: str) -> None:
        if not guess.isalpha():
            raise WordleException(f"Invalid guess: At least one of the characters in '{guess}' is not alphabetic.")
        if len(guess) != 5:
            raise WordleException(f"Invalid guess: '{guess}' does not have 5 letters.")
        if guess not in AllWords.words:
            raise WordleException(f"Invalid guess: '{guess}' is not a word.")

    async def validate_game_status(self) -> None:
        if await self.game.status == GameStatus.FINISHED:
            raise WordleException("Game is over!")

    async def get_guess_result(self) -> GuessResult:
        if await self.game.result == GameResult.VICTORY:
            return GuessResult.GUESSED
        return GuessResult.NOT_GUESSED

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
