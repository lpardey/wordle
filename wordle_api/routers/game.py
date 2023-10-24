from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, status
from wordle_api.models import Game, User
from wordle_api.schemas import (
    BasicStatus,
    CreateGameRequest,
    CreateGameResponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
)
from wordle_api.schemas.game import GameStatusResponse
from wordle_api.services.authentication import get_current_active_user
from wordle_client.game_word import AllWords, get_game_word
from wordle_api.services.game import WordleException, WordleGame
import logging

logger = logging.getLogger("Game")

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/create")
async def create_game(current_user: Annotated[User, Depends(get_current_active_user)]) -> CreateGameResponse:
    create_game_request = CreateGameRequest(user_id=current_user.id)
    try:
        game_word = get_game_word(words_list=AllWords.words)
        game = await Game.create(
            user_id=create_game_request.user_id,
            game_word=game_word,
            max_attempts=create_game_request.game_config.number_of_attempts,
            difficulty=create_game_request.game_config.game_difficulty,
        )
        return CreateGameResponse(game_id=game.id)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/status/{game_id}")
async def get_game_status(
    game_id: int, current_user: Annotated[User, Depends(get_current_active_user)]
) -> GameStatusResponse:
    game = await Game.get_or_none(id=game_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Game not found")
    return GameStatusResponse(
        id=game.id,
        game_word=game.game_word,
        guesses_left=await game.guesses_left,
        status=await game.status,
        result=await game.result,
        difficulty=game.difficulty,
        creation_date=game.creation_date,
        guesses=await game.guesses.all().values_list("value", flat=True),
    )


@router.post("/guess/{game_id}")
async def take_a_guess(
    game_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    guess_request: TakeAGuessRequest,
) -> TakeAGuessResponse:
    game = await Game.get_or_none(id=game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    guess = guess_request.guess.upper()
    wordle_game = WordleGame(game)
    game_status = BasicStatus.OK
    message = None
    guess_result = None
    guess_letters_status = None
    try:
        guess_result = await wordle_game.guess(guess)
        guess_letters_status = wordle_game.compare(guess, wordle_game.game.game_word)
    except WordleException as e:
        game_status = BasicStatus.ERROR
        message = str(e)
    return TakeAGuessResponse(
        status=game_status,
        message=message,
        guess_result=guess_result,
        guess_letters_status=guess_letters_status,
    )
