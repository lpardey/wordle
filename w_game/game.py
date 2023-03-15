from w_game.game_state import GameState, Guess

# schema = transferir informacion --- esto va en la API
# modelo = almacenar informacion --- esto va en la base de datos



class WordleGame():
    def __init__(self, game_state: GameState, guess: Guess) -> None:
        self.game_state = game_state

