from tortoise.models import Model
from tortoise import fields
from wordle_game.game_enums import GameDifficulty, GameResult, GameStatus
from .guess import Guess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Game(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("models.User", related_name="games")
    game_word = fields.CharField(max_length=5)
    max_attempts = fields.SmallIntField()
    difficulty = fields.IntEnumField(enum_type=GameDifficulty)
    creation_date = fields.DatetimeField(auto_now_add=True)
    guesses: fields.ReverseRelation["Guess"]

    def __str__(self) -> str:
        return f"Game {self.id} for user {self.user.id} created: {self.creation_date}"

    @property
    async def guesses_left(self) -> int:
        return self.max_attempts - await self.guesses.all().count()

    @property
    async def status(self) -> GameStatus:
        if await self.guesses_left > 0 and await self.result != GameResult.VICTORY:
            return GameStatus.WAITING_FOR_GUESS
        return GameStatus.FINISHED

    @property
    async def result(self) -> GameResult | None:
        guesses_left = await self.guesses_left
        last_guess = await self.guesses.all().order_by("-id").first()
        if last_guess is None:
            return None
        if guesses_left > 0 and last_guess.value != self.game_word:
            return None
        if last_guess.value == self.game_word:
            return GameResult.VICTORY
        return GameResult.DEFEAT
