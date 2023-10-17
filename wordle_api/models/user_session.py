from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class UserSession(Model):
    id = fields.IntField(pk=True)
    access_token = fields.CharField(max_length=255)
    creation_date = fields.DatetimeField(auto_now_add=True)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("models.User", related_name="sessions")
