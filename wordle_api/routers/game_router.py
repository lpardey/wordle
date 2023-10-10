from fastapi import HTTPException, APIRouter, status
from wordle_api.models import Game, Game_Pydantic
from wordle_api.schemas.game_schemas import (
    BasicStatus,
    CreateGameRequest,
    CreateGameResponse,
    GameStatusInfo,
    GameStatusResponse,
    TakeAGuessRequest,
    TakeAGuessResponse,
)
from wordle_client.game_word import AllWords, get_game_word
from wordle_game.game import WordleException, WordleGame
from wordle_game.game_state import GameState

# from wordle_api.user.auth import authorized_endpoint

router = APIRouter(prefix="/game", tags=["Game"])


@router.get("/{game_id}")
# @authorized_endpoint
async def get_game_status(game_id: int) -> GameStatusResponse:
    game = await Game.get_or_none(id=game_id)
    if game is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Game not found")
    # a = await Game_Pydantic.from_tortoise_orm(game)
    response = GameStatusResponse(
        game_status_info=GameStatusInfo(
            game_word=game.game_word,
            guesses=await game.guesses.all(),
            attempts_left=await game.guesses_left,
            game_status=await game.status,
            difficulty=game.difficulty,
        )
    )
    return response
    # return a


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
    # game = await Game_Pydantic.from_tortoise_orm(game_query)
    guess = guess_request.guess.upper()
    game_state = GameState(
        player_id=user_id,
        game_word=game_query.game_word,
        guesses=await game_query.guesses,
        number_of_attempts=await game_query.guesses_left,
        result=await game_query.result,
        difficulty=game_query.difficulty,
        game_creation_date=game_query.game_creation_date,
    )
    wordle = WordleGame(game_state)
    game_status = BasicStatus.OK
    message = None
    guess_result = None
    guess_letters_status = None
    try:
        guess_result = wordle.guess(guess=guess)
        guess_letters_status = wordle.compare(guess, game_query.game_word)
    except WordleException as e:
        game_status = BasicStatus.ERROR
        message = str(e)
    # a = await Game_Pydantic.from_tortoise_orm(game_query)
    # game_query.update_from_dict(a.model_dump())
    return TakeAGuessResponse(
        status=game_status, message=message, guess_result=guess_result, guess_letters_status=guess_letters_status
    )


# @router.post("/{player_id}/{game_id}/guess")
# def take_a_guess(player_id: int, game_id: int, guess_request: TakeAGuessRequest) -> TakeAGuessResponse:
#     game_state = GAME_STORAGE.get_game_state(game_id=game_id)

#     if game_state.player_id != player_id:
#         raise HTTPException(status_code=403, detail="FORBIDDEN")

#     wordle = WordleGame(game_state)
#     guess = guess_request.guess.upper()
#     game_word = wordle.game_state.game_word
#     status = BasicStatus.OK
#     message = None
#     guess_result = None
#     guess_letters_status = None

#     try:
#         guess_result = wordle.guess(guess=guess)
#         guess_letters_status = wordle.compare(guess=guess, word=game_word)

#     except WordleException as e:
#         status = BasicStatus.ERROR
#         message = str(e)

#     response = TakeAGuessResponse(
#         status=status, message=message, guess_result=guess_result, guess_letters_status=guess_letters_status
#     )
#     return response
