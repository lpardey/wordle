from tortoise.models import Model
from tortoise import fields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game


class Guess(Model):
    id = fields.IntField(pk=True)
    value = fields.CharField(max_length=5)
    game: fields.ForeignKeyRelation["Game"] = fields.ForeignKeyField("models.Game", related_name="guesses")
