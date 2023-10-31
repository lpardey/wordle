# Dependencies
from fastapi import status
from fastapi.exceptions import HTTPException
from tortoise.exceptions import BaseORMException

# From apps
from wordle_api.models.game import Game


async def get_game_by_id(game_id: int) -> Game:
    try:
        game = await Game.get_or_none(id=game_id)
    except BaseORMException as e:
        detail = f"Error while querying the database: {e}"
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Game not found")

    return game
