from pydantic import BaseModel
from wordle_game.player_statistics import PlayerStatistics


class Player(BaseModel):
    player_name: str = "Guillermo"
    password: str = "12345"
    can_play: bool = True
    statistics: PlayerStatistics

    class Config:
        arbitrary_types_allowed = True
