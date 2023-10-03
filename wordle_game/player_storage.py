from fastapi import HTTPException, status
from wordle_game.game_state import GameState
from wordle_game.game_storage import GameStorage
from wordle_game.player import Player


ALL_PLAYERS: dict[int, Player] = {}


class PlayerStorage:
    def __init__(self, storage: dict[int, Player] = ALL_PLAYERS) -> None:
        self.storage = storage

    def get_player(self, player_id: int) -> Player | None:
        player = self.storage.get(player_id)
        return player

    def get_player_id(self, user: Player) -> int | None:
        for player_id, player in self.storage.items():
            if user == player:
                return player_id

    def add_player(self, player: Player) -> int:
        index = self.storage_size()
        self.storage[index] = player
        return index

    def storage_size(self) -> int:
        storage_size = len(self.storage)
        return storage_size

    def reset_storage(self) -> None:
        self.storage.clear()


def get_player_by_id(player_id: int) -> Player:
    player = PlayerStorage().get_player(player_id=player_id)

    if player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return player


def get_game_state_by_id(game_id: int) -> GameState:
    game_storage = GameStorage()
    game_state = game_storage.get_game_state(game_id=game_id)

    if game_state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return game_state
