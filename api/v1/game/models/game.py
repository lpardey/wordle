# Standard Library
from typing import TYPE_CHECKING

# Dependencies
from tortoise import fields
from tortoise.models import Model

# From apps
from api.v1.game.services.resources.schemas import GameDifficulty, GameResult, GameStatus

if TYPE_CHECKING:
    # From apps
    from api.v1.user.models import User

    # Local imports
    from . import Guess


class Game(Model):
    id = fields.UUIDField(pk=True)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("models.User", related_name="games")
    game_word = fields.CharField(max_length=5)
    max_attempts = fields.SmallIntField()
    difficulty = fields.CharEnumField(enum_type=GameDifficulty)
    creation_date = fields.DatetimeField(auto_now_add=True)
    finished_date = fields.DatetimeField(null=True, default=None)
    guesses: fields.ReverseRelation["Guess"]

    def __str__(self) -> str:
        return f"""Game {self.id}
        Creation date: {self.creation_date.strftime('%B %d of %Y')}"""

    @property
    async def guesses_left(self) -> int:
        return self.max_attempts - await self.guesses.all().count()

    @property
    async def result(self) -> GameResult | None:
        guesses_left = await self.guesses_left
        last_guess = await self.guesses.all().order_by("-creation_date").first()

        if last_guess is None:
            return None
        if guesses_left > 0 and last_guess.value["guess"] != self.game_word:
            return None
        if last_guess.value["guess"] == self.game_word:
            return GameResult.VICTORY

        return GameResult.DEFEAT

    @property
    async def status(self) -> GameStatus:
        guesses_left = await self.guesses_left
        game_result = await self.result

        if guesses_left > 0 and game_result != GameResult.VICTORY:
            return GameStatus.WAITING_FOR_GUESS

        return GameStatus.FINISHED

    @property
    async def in_game_word(self) -> str | None:
        game_status = await self.status

        if game_status == GameStatus.FINISHED:
            return self.game_word
