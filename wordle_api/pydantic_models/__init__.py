# Dependencies
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

# From apps
from wordle_api.models import Game, Guess, User, UserSession

Tortoise.init_models(["wordle_api.pydantic_models", "wordle_api.models"], "models")
User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password_hash",))
UserSession_Pydantic = pydantic_model_creator(UserSession, name="User Session", exclude=("user.password_hash",))
Game_Pydantic = pydantic_model_creator(Game, name="Game", exclude=("user.password_hash",))
Guess_Pydantic = pydantic_model_creator(Guess, name="Guess")
