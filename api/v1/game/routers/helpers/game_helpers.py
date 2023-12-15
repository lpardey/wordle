# Standard Library
from asyncio import gather
from uuid import UUID

# Dependencies
from fastapi import status
from fastapi.exceptions import HTTPException
from tortoise.exceptions import BaseORMException

# From apps
from api.v1.game.models.game import Game
from api.v1.game.schemas.game import GameState


async def get_game_by_id(game_id: UUID) -> Game:
    try:
        game = await Game.get_or_none(id=game_id)
    except BaseORMException as e:
        detail = f"Error while querying the database: {e}"
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Game not found")

    return game


async def get_game_state(game: Game, guess: str) -> GameState:
    status, result = await gather(game.status, game.result)
    return GameState(id=game.id, game_word=game.game_word, guess=guess, status=status, result=result)
