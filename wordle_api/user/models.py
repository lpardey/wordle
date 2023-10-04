from tortoise.models import Model
from tortoise import fields
from wordle_api.game.models import Game


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20)
    password = fields.CharField(max_length=20)
    disabled = fields.BooleanField(default=False)

    games: fields.ReverseRelation["Game"]
    sessions: fields.ReverseRelation["UserSession"]


class UserSession(Model):
    session_id = fields.IntField(pk=True)
    user_id = fields.ForeignKeyField("User", related_name="sessions")
    token = fields.CharField(max_length=20)
    expiration_date = fields.DatetimeField()
