# Standard Library
import logging
from typing import Annotated
from uuid import UUID

# Dependencies
from fastapi import APIRouter, Depends, HTTPException, Path, status
from tortoise.exceptions import BaseORMException

# From apps
from api.v1.game.models import Game, Guess
from api.v1.game.routers.helpers.game_helpers import get_game_by_id, get_game_state
from api.v1.game.schemas.game import (
    BasicStatus,
    CreateGameRequest,
    CreateGameResponse,
    GameStatusResponse,
    GuessValue,
    TakeAGuessRequest,
    TakeAGuessResponse,
)
from api.v1.game.services.authentication import get_current_active_user
from api.v1.game.services.game import WordleException, WordleGame
from api.v1.game.services.resources.game_word import AllWords, get_game_word
from api.v1.user.models import User

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


@router.get("/status/last_game")
async def get_last_game_status(current_user: Annotated[User, Depends(get_current_active_user)]) -> GameStatusResponse:
    last_game = await current_user.games.all().order_by("-creation_date").first()
    last_game_status = await get_game_status(last_game.id, current_user)
    return last_game_status


@router.get("/status/{game_id}")
async def get_game_status(
    game_id: Annotated[UUID, Path(title="Game ID")],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> GameStatusResponse:
    game = await get_game_by_id(game_id)
    return GameStatusResponse(
        id=game.id,
        game_word=await game.in_game_word,
        guesses_left=await game.guesses_left,
        max_attempts=game.max_attempts,
        difficulty=game.difficulty,
        creation_date=game.creation_date,
        guesses=await game.guesses.all().values_list("value", flat=True),
        result=await game.result,
        status=await game.status,
        finished_date=game.finished_date,
    )


@router.post("/guess/{game_id}")
async def take_a_guess(
    game_id: Annotated[UUID, Path(title="Game ID")],
    current_user: Annotated[User, Depends(get_current_active_user)],
    guess_request: TakeAGuessRequest,
) -> TakeAGuessResponse:
    game = await get_game_by_id(game_id)
    guess = guess_request.guess.upper()
    game_state = await get_game_state(game, guess)
    wordle_game = WordleGame(game_state)
    game_status = BasicStatus.OK
    message = None
    guess_result = None
    letters_status = None
    try:
        guess_result = wordle_game.guess()
        letters_status = wordle_game.compare()
        guess_value_json = GuessValue(guess=guess, letters_status=letters_status).model_dump_json()
        await Guess.create(game_id=game_state.id, value=guess_value_json)
        await game.save()  # To trigger the game signals
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
