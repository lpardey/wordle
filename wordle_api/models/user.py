from tortoise import fields
from tortoise.models import Model
from .game import Game
from .user_session import UserSession


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=100)
    disabled = fields.BooleanField(default=False)
    creation_date = fields.DatetimeField(auto_now_add=True)
    games: fields.ReverseRelation["Game"]
    sessions: fields.ReverseRelation["UserSession"]
