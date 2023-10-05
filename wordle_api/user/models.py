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

    class Meta:
        table = "User"
        table_description = "Information regarding a user"

    def __str__(self) -> str:
        return f"User {self.id}: '{self.username}'"


class UserSession(Model):
    session_id = fields.IntField(pk=True)
    user_id = fields.ForeignKeyField("models.User", related_name="sessions")
    token = fields.CharField(max_length=20)
    session_creation_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "User Session"
        table_description = "Information regarding a user's session"

    def __str__(self) -> str:
        message = f"Session {self.session_id} for user {self.user_id} created: {self.session_creation_date}"
        return message
