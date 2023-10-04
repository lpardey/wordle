from tortoise.models import Model
from tortoise import fields


class Game(Model):
    id = fields.IntField(pk=True)
    player_id = fields.IntField()
    game_word = fields.CharField(max_length=5)
    guesses = []
    number_of_attempts = fields.IntField()
    result = fields.CharEnumField()
    difficulty = fields.CharEnumField()
    game_creation_date = fields.DatetimeField()

    def __str__(self) -> str:
        return f"Game {self.id}: {self.game_creation_date}"

    class Meta:
        schema = "Game State"
        table = "Game State"
        table_description = "Information regarding a game state"


class Guess(Model):
    id = fields.IntField(pk=True)
    game_id = fields.ForeignKeyField("models.Game", related_name="guess")
    value = fields.CharField(max_length=5)
    letters_status = []


# class GameState(BaseModel):
#     player_id: int
#     game_word: str
#     guesses: list[str] = []
#     number_of_attempts: int = 6
#     result: GameResult = GameResult.DEFEAT
#     difficulty: GameDifficulty = GameDifficulty.NORMAL
#     game_creation_date: datetime
