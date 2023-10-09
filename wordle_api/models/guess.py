from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Guess(Model):
    id = fields.IntField(pk=True)
    game = fields.ForeignKeyField("models.Game", related_name="guesses")
    value = fields.CharField(max_length=5)

    def __str__(self) -> str:
        return f"Guess {self.id} for game {self.game_id}: '{self.value}'"


Guess_Pydantic = pydantic_model_creator(Guess, name="Guess")
