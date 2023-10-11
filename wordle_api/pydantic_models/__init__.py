from tortoise.contrib.pydantic import pydantic_model_creator
from wordle_api.models import Game, Guess, UserSession, User
from tortoise import Tortoise

Tortoise.init_models(["wordle_api.pydantic_models", "wordle_api.models"], "models")
User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password",))
UserSession_Pydantic = pydantic_model_creator(UserSession, name="User Session", exclude=("user.password",))
Game_Pydantic = pydantic_model_creator(Game, name="Game", exclude=("user.password",))
Guess_Pydantic = pydantic_model_creator(Guess, name="Guess")
