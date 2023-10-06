from tortoise import fields
from tortoise.models import Model


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
