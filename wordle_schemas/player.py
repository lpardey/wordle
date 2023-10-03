from pydantic import BaseModel


class PlayerCreationResponse(BaseModel):
    player_id: int
