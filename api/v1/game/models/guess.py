# Standard Library
from typing import TYPE_CHECKING

# Dependencies
from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    # Local imports
    from .game import Game


class Guess(Model):
    id = fields.UUIDField(pk=True)
    value = fields.JSONField()
    game: fields.ForeignKeyRelation["Game"] = fields.ForeignKeyField("models.Game", related_name="guesses")
    creation_date = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Guess {self.id}: {self.value}"
