# Standard Library
from typing import TYPE_CHECKING

# Dependencies
from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    # Local imports
    from .game import Game


class Guess(Model):
    id = fields.IntField(pk=True)
    value = fields.CharField(max_length=5)
    game: fields.ForeignKeyRelation["Game"] = fields.ForeignKeyField("models.Game", related_name="guesses")

    def __str__(self) -> str:
        return f"Guess {self.id}: {self.value}"