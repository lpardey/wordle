from wordle_game.game_state import GameState


ALL_GAMES: dict[int, GameState] = {}


class GameStorage:
    def __init__(self, storage: dict[int, GameState] = ALL_GAMES) -> None:
        self.storage = storage

    def get_game_state(self, game_id: int) -> GameState | None:
        game_state = self.storage.get(game_id)
        return game_state

    def get_game_id(self, game_state: GameState) -> int | None:
        for key, game in self.storage.items():
            if game == game_state:
                return key

    def add_game_state(self, game_state: GameState) -> int:
        index = self.storage_size()
        self.storage[index] = game_state
        return index

    def storage_size(self) -> int:
        storage_size = len(self.storage)
        return storage_size

    def reset_storage(self) -> None:
        self.storage.clear()

    def get_all_games_by_player(self, player_id: int) -> list[GameState]:
        games = [game_state for game_state in self.storage.values() if game_state.player_id == player_id]
        return games


# TODO: manejo de base de datos con tortoise
# ALL_GAME_ID_TO_PLAYER_ID_RELATIONSHIPS: dict[int, int] = {}

# class GameIdToPlayerIdStorage:
#     ...

# ALL_GAMES: dict[int, GameState] = {}

# class GameStorage:
#     def __init__(self, storage: dict[int, GameState] = ALL_GAMES) -> None:
#         self.storage = storage

#     def get_game_state(self, index: int) -> GameState | None:
#         game_state = self.storage.get(index)
#         return game_state

#     def get_game_id(self, game_state: GameState) -> int | None:
#         for key, game in self.storage.items():
#             if game == game_state:
#                 return key

#     def add_game_state(self, game_state: GameState) -> int:
#         index = self.storage_size()
#         self.storage[index] = game_state
#         return index

#     def storage_size(self) -> int:
#         storage_size = len(self.storage)
#         return storage_size

#     def reset_storage(self) -> None:
#         self.storage.clear()


# def get_game_state_by_id(game_id: int) -> GameState:
#     game_state = GameStorage().get_game_state(index=game_id)

#     if game_state is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     return game_state
