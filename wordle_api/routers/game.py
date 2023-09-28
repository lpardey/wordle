from fastapi import HTTPException, APIRouter, Request
from wordle_client.game_word import AllWords, get_game_word
from wordle_game.game import WordleException, WordleGame
from wordle_game.game_storage import GameStorage
from wordle_game.player_storage import get_game_state_by_id, get_player_by_id
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

from wordle_api.user.auth import authorized_endpoint

router = APIRouter(prefix="/game", tags=["Game"])


@router.get("/{game_id}")
# @authorized_endpoint
def get_game_status(request: Request, game_id: int) -> GameStatusResponse:
    game_state = get_game_state_by_id(game_id=game_id)
    wordle = WordleGame(game_state=game_state)
    guesses = [
        Guess(word=guess, letters_status=wordle.compare(guess, game_state.game_word)) for guess in game_state.guesses
    ]
    response = GameStatusResponse(
        game_status_info=GameStatusInfo(
            game_word=game_state.game_word,
            guesses=guesses,
            attempts_left=game_state.guesses_left,
            game_status=game_state.status,
            difficulty=game_state.difficulty,
        )
    )
    return response


@router.post("/{player_id}")
def create_game(player_id: int, game_config: GameConfig) -> GameCreationResponse:
    game_state = GameState(
        player_id=player_id,
        game_word=get_game_word(words_list=AllWords.words),
        number_of_attempts=game_config.number_of_attempts,
        difficulty=game_config.game_difficulty,
    )
    game_id = GameStorage().add_game_state(game_state=game_state)
    return GameCreationResponse(game_id=game_id)


@router.post("/{player_id}/{game_id}/guess")
def take_a_guess(player_id: int, game_id: int, guess_request: TakeAGuessRequest) -> TakeAGuessResponse:
    game_state = get_game_state_by_id(game_id=game_id)

    if game_state.player_id != player_id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

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
