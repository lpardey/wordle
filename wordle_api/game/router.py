from fastapi import FastAPI
from wordle_game.game import WordleException, WordleGame
from wordle_game.game_storage import GameStorage, get_game_state_by_id
from wordle_schemas.game import (
    BasicStatus,
    GameCreationResponse,
    GameConfig,
    GameStatusInfo,
    GameStatusResponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
)
from wordle_game.game_state import GameState, GuessResult

app = FastAPI()


@app.get("/game/{game_id}")
def get_game_state(game_id: int) -> GameStatusResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    response = GameStatusResponse(
        game_status_info=GameStatusInfo(
            game_word=game_state.game_word,
            guesses=game_state.guesses,
            game_status=game_state.status,
            difficulty=game_state.difficulty,
        )
    )
    return response


@app.post("/game")
def create_game(game_config: GameConfig) -> GameCreationResponse:
    game_storage = GameStorage()
    game_state = GameState(
        user_id=0,
        game_word="PIZZA",
        number_of_attempts=game_config.number_of_attempts,
        difficulty=game_config.game_difficulty,
    )
    game_id = game_storage.add_game_state(game_state=game_state)
    return GameCreationResponse(game_id=game_id)


@app.post("/game/{game_id}/guess")
def take_a_guess(game_id: int, guess_request: TakeAGuessRequest) -> TakeAGuessResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    wordle = WordleGame(game_state)
    status = BasicStatus.OK
    message = None
    guess_result = GuessResult.NOT_GUESSED

    try:
        guess_result = wordle.guess(guess=guess_request.guess.upper())

    except WordleException as e:
        status = BasicStatus.ERROR
        message = str(e)

    response = TakeAGuessResponse(status=status, message=message, guess_result=guess_result)
    return response
