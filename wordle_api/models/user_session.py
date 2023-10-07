from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class UserSession(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="sessions")
    token = fields.CharField(max_length=255)
    session_creation_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "User Session"
        table_description = "Information regarding a user's session"

    def __str__(self) -> str:
        message = f"Session {self.id} for user {self.user} created: {self.session_creation_date}"
        return message


UserSession_Pydantic = pydantic_model_creator(UserSession, name="User Session")
