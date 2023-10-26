# Dependencies
from fastapi import HTTPException, status

# From apps
from wordle_api.models.game import Game


async def get_game_by_id(game_id: int) -> Game:
    game = await Game.get_or_none(id=game_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game
