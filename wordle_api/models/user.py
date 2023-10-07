from tortoise import fields
from tortoise.models import Model
from .game import Game
from .user_session import UserSession
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    disabled = fields.BooleanField(default=False)

    games: fields.ReverseRelation["Game"]
    sessions: fields.ReverseRelation["UserSession"]

    class Meta:
        table = "User"
        table_description = "Information regarding a user"

    def __str__(self) -> str:
        return f"User {self.id}: '{self.username}'"


User_Pydantic = pydantic_model_creator(User, name="User")
