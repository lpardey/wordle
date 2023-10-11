from fastapi import HTTPException, APIRouter, status
from wordle_api.models import Game
from wordle_api.pydantic_models import Game_Pydantic
from wordle_api.schemas.game_schemas import (
    BasicStatus,
    CreateGameRequest,
    CreateGameResponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
)
from wordle_client.game_word import AllWords, get_game_word
from wordle_game.game import WordleException, WordleGame

# from wordle_api.user.auth import authorized_endpoint

router = APIRouter(prefix="/game", tags=["Game"])


@router.get("/{game_id}", response_model=Game_Pydantic)
# @authorized_endpoint
async def get_game_status(game_id: int):
    game = await Game.get_or_none(id=game_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Game not found")
    return await Game_Pydantic.from_tortoise_orm(game)


@router.post("/{user_id}")
async def create_game(create_game_request: CreateGameRequest) -> CreateGameResponse:
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
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{user_id}/{game_id}/guess")
async def take_a_guess(user_id: int, game_id: int, guess_request: TakeAGuessRequest) -> TakeAGuessResponse:
    game_query = await Game.get_or_none(id=game_id, user_id=user_id)
    if game_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    guess = guess_request.guess.upper()
    wordle_game = WordleGame(game_query)
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
