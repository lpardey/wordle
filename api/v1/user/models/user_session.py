# Standard Library
from typing import TYPE_CHECKING

# Dependencies
from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    # From apps
    from api.v1.user.models import User


class UserSession(Model):
    id = fields.IntField(pk=True)
    access_token = fields.CharField(max_length=255)
    creation_date = fields.DatetimeField(auto_now_add=True)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("models.User", related_name="sessions")

    def __str__(self) -> str:
        message = f"""Session {self.id}
        Creation date: {self.creation_date.strftime('%B %d of %Y')}"""
        return message
