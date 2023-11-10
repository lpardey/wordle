# Standard Library
from typing import TYPE_CHECKING

# Dependencies
from tortoise import fields
from tortoise.models import Model

# From apps
# from api.v1.game.models import Game
from api.v1.game.services.resources.schemas import GameStatus

if TYPE_CHECKING:
    # From apps
    from api.v1.game.models import Game

    # Local imports
    from . import UserSession


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=100)
    disabled = fields.BooleanField(default=False)
    creation_date = fields.DatetimeField(auto_now_add=True)
    games: fields.ReverseRelation["Game"]
    sessions: fields.ReverseRelation["UserSession"]

    def __str__(self) -> str:
        message = f"""User {self.id}: '{self.username}'
        Creation date: {self.creation_date.strftime('%B %d of %Y')}"""
        return message

    @property
    async def ongoing_game(self) -> bool:
        last_game = await self.games.all().order_by("-id").first()
        last_game_status = await last_game.status

        if last_game and last_game_status == GameStatus.WAITING_FOR_GUESS:
            return True

        return False
