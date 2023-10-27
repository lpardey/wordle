# Standard Library
import logging
from typing import Annotated

# Dependencies
from fastapi import APIRouter, Depends, HTTPException, Path, status

# From apps
from wordle_api.models import Game, User
from wordle_api.models.guess import Guess
from wordle_api.routers.helpers.game_helpers import get_game_by_id
from wordle_api.schemas import (
    BasicStatus,
    CreateGameRequest,
    CreateGameResponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
    GameState,
    GameStatusResponse,
)
from wordle_api.services.authentication import get_current_active_user
from wordle_api.services.game import WordleException, WordleGame
from wordle_client.game_word import AllWords, get_game_word

logger = logging.getLogger("Game")

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
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
        return CreateGameResponse(game_id=game.id, creation_date=game.creation_date)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/status/{game_id}")
async def get_game_status(
    game_id: Annotated[int, Path(title="Game ID")],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> GameStatusResponse:
    game = await get_game_by_id(game_id)
    return GameStatusResponse(
        id=game.id,
        game_word=game.game_word,
        guesses_left=await game.guesses_left,
        status=await game.status,
        difficulty=game.difficulty,
        creation_date=game.creation_date,
        guesses=await game.guesses.all().values_list("value", flat=True),
        result=await game.result,
        finished_date=await game.finished_date,
    )


@router.post("/guess/{game_id}")
async def take_a_guess(
    game_id: Annotated[int, Path(title="Game ID")],
    current_user: Annotated[User, Depends(get_current_active_user)],
    guess_request: TakeAGuessRequest,
) -> TakeAGuessResponse:
    game = await get_game_by_id(game_id)
    game_state = GameState(
        id=game_id,
        game_word=game.game_word,
        guess=guess_request.guess.upper(),
        status=await game.status,
        result=await game.result,
    )
    wordle_game = WordleGame(game_state)
    game_status = BasicStatus.OK
    message = None
    guess_result = None
    letters_status = None
    try:
        guess_result = wordle_game.guess()
        await Guess.create(game_id=game_state.id, value=game_state.guess)
        letters_status = wordle_game.compare()
    except WordleException as e:
        game_status = BasicStatus.ERROR
        message = str(e)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return TakeAGuessResponse(
        status=game_status,
        message=message,
        guess_result=guess_result,
        letters_status=letters_status,
    )
