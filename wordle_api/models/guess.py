from tortoise.models import Model
from tortoise import fields


class Guess(Model):
    id = fields.IntField(pk=True)
    game_id = fields.ForeignKeyField("models.Game", related_name="guesses")
    value = fields.CharField(max_length=5)

    class Meta:
        table = "Guess"
        table_description = "Information regarding a guess"

    def __str__(self) -> str:
        return f"Guess {self.id} for game {self.game_id}: '{self.value}'"
