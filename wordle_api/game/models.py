from wordle_game.game_state import GameResult, GameDifficulty, GameStatus
from tortoise.models import Model
from tortoise import fields


class Game(Model):
    id = fields.IntField(pk=True)
    player_id = fields.ForeignKeyField("models.User", related_name="games")
    game_word = fields.CharField(max_length=5)
    max_attempts = fields.IntField()
    difficulty = fields.CharEnumField(GameDifficulty)
    game_creation_date = fields.DatetimeField(auto_now_add=True)
    guesses: fields.ReverseRelation["Guess"]

    def __str__(self) -> str:
        return f"Game {self.id} for user {self.player_id} created: {self.game_creation_date}"

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

    class Meta:
        table = "Game"
        table_description = "Information regarding a game"


class Guess(Model):
    id = fields.IntField(pk=True)
    game_id = fields.ForeignKeyField("models.Game", related_name="guesses")
    value = fields.CharField(max_length=5)

    class Meta:
        table = "Guess"
        table_description = "Information regarding a guess"

    def __str__(self) -> str:
        return f"Guess {self.id} for game {self.game_id}: '{self.value}'"
