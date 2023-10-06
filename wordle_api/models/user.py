from tortoise import fields
from tortoise.models import Model
from .game import Game
from .user_session import UserSession


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20)
    password = fields.CharField(max_length=20)
    disabled = fields.BooleanField(default=False)

    games: fields.ReverseRelation["Game"]
    sessions: fields.ReverseRelation["UserSession"]

    class Meta:
        table = "User"
        table_description = "Information regarding a user"

    def __str__(self) -> str:
        return f"User {self.id}: '{self.username}'"
