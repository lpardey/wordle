from fastapi import FastAPI
from wordle_game.game import WordleException, WordleGame
from wordle_game.game_storage import GameStorage, get_game_state_by_id
from wordle_schemas.game import (
    BasicStatus,
    GameCreationResponse,
    GameConfig,
    GameStatusInfo,
    GameStatusResponse,
    Guess,
    TakeAGuessRequest,
    TakeAGuessResponse,
)
from wordle_game.game_state import GameState

app = FastAPI()


@app.get("/game/{game_id}")
def get_game_status(game_id: int) -> GameStatusResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    wordle = WordleGame(game_state=game_state)
    guesses = [
        Guess(word=guess, letters_status=wordle.compare(guess, game_state.game_word)) for guess in game_state.guesses
    ]
    response = GameStatusResponse(
        game_status_info=GameStatusInfo(
            game_word=game_state.game_word,
            guesses=guesses,
            game_status=game_state.status,
            attempts_left=game_state.guesses_left,
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
    guess = guess_request.guess.upper()
    game_word = wordle.game_state.game_word
    status = BasicStatus.OK
    message = None
    guess_result = None
    guess_letters_status = None

    try:
        guess_result = wordle.guess(guess=guess)
        guess_letters_status = wordle.compare(guess=guess, word=game_word)

    except WordleException as e:
        status = BasicStatus.ERROR
        message = str(e)

    response = TakeAGuessResponse(
        status=status, message=message, guess_result=guess_result, guess_letters_status=guess_letters_status
    )
    return response
