from pydantic import BaseModel

# Cuando el jugador gane o pierda el game state se debe resetear
# Si gana puede seguir jugando, si pierde debe esperar 24 horas.


class PlayerStatistics(BaseModel):
    games_played: int = 0
    winning_rate: float = 0
    current_streak: int = 0
    max_streak: int = 0
    guesses_on_attemp: dict[int, int] = {key: value - value for key, value in enumerate(range(6), start=1)}


# pa despues porque guille dijo : (
# class GameResult(BaseModel):
#     game_word: str
#     guesses: list[str]
#     guess_result: GuessResult
#     current_streak: int


# class GameStatistics(BaseModel):
#     game_results: list[GameResult]
#     games_played: int
#     winning_percentage: int
#     max_streak: int
