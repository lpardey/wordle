# Standard Library
import logging
from typing import Annotated

# Dependencies
from fastapi import APIRouter, Depends, HTTPException, Path, status
from tortoise.exceptions import BaseORMException

# From apps
from wordle_api.models import Game, User
from wordle_api.models.guess import Guess
from wordle_api.routers.helpers.game_helpers import get_game_by_id
from wordle_api.schemas import (
    BasicStatus,
    CreateGameRequest,
    CreateGameResponse,
    GameState,
    GameStatusResponse,
    OnGoingGameReponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
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
    except BaseORMException as e:
        detail = f"Error while querying the database: {e}"
        logger.exception(detail)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
    except Exception as e:
        detail = f"Unexpected error: {e}"
        logger.exception(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


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
    except BaseORMException as e:
        detail = f"Error while querying the database: {e}"
        logger.exception(detail)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    return TakeAGuessResponse(
        status=game_status,
        message=message,
        guess_result=guess_result,
        letters_status=letters_status,
    )


@router.get("/ongoing_game")
async def get_ongoing_game(current_user: Annotated[User, Depends(get_current_active_user)]) -> OnGoingGameReponse:
    ongoing_game = await current_user.ongoing_game
    if ongoing_game:
        current_game = await current_user.games.all().order_by("-id").first()
        game_status = await get_game_status(game_id=current_game.id, current_user=current_user)
    else:
        game_status = None
    return OnGoingGameReponse(ongoing_game=ongoing_game, game_status=game_status)


# @router.get("last_game")
# async def get_last_game(current_user: Annotated[User, Depends(get_current_active_user)]) -> LastGameResponse | None:
#     last_game = await current_user.games.all().order_by("-id").first()
#     if last_game:
#         return LastGameResponse(game_id=await last_game.id, finished_date=await last_game.finished_date)
