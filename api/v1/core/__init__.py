# Dependencies
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

# From apps
from api.v1.game.models import Game, Guess
from api.v1.user.models import User, UserSession

Tortoise.init_models(["api.v1.game.models", "api.v1.user.models"], "models")
User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password_hash",))
UserSession_Pydantic = pydantic_model_creator(UserSession, name="User Session", exclude=("user.password_hash",))
Game_Pydantic = pydantic_model_creator(Game, name="Game", exclude=("user.password_hash",))
Guess_Pydantic = pydantic_model_creator(Guess, name="Guess")
