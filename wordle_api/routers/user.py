from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from wordle_api.schemas.user import SignUpRequest, SignUpResponse
from wordle_api.services.authentication import create_access_token, get_current_active_user
from wordle_api.services.resources.utils import AuthException, get_password_hash, authenticate_user
from wordle_api.pydantic_models import User_Pydantic, UserSession_Pydantic
from wordle_api.models import User, UserSession

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/get", response_model=User_Pydantic)
async def get_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await User_Pydantic.from_tortoise_orm(current_user)


# @router.get("/get", response_model=User_Pydantic)
# async def get_user(username: str):
#     user_query = await User.get_or_none(username=username)
#     if user_query is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with {username=} not found")
#     user = await User_Pydantic.from_tortoise_orm(user_query)
#     return user


@router.post("/create")
async def create_user(request: SignUpRequest) -> SignUpResponse:
    if await User.exists(username=request.username):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Username unavailable")
    try:
        password = request.password.get_secret_value()
        password_hash = get_password_hash(password)
        user = await User.create(username=request.username, password_hash=password_hash)
        return SignUpResponse(user_id=user.id)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login", response_model=UserSession_Pydantic)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        access_token = create_access_token(data={"sub": user.username})
        session = await UserSession.create(token=access_token, user_id=user.id)
        return await UserSession_Pydantic.from_tortoise_orm(session)
    except AuthException:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# @router.post("/login", response_model=UserSession_Pydantic)
# async def login(request: LoginRequest):
#     try:
#         password = request.password.get_secret_value()
#         user = await authenticate_user(request.username, password)
#         token = "auth token"
#         session = await UserSession.create(user_id=user.id, token=token)
#         return await UserSession_Pydantic.from_tortoise_orm(session)
#     except AuthException:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")
#     except Exception as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


#   1. Front send a post to /get to get user data
#   if user has an ongoing game:
#       2. Front Redirects to game

# UserLoginForm
#   1. Front sends a post to /login to create a UserSession
#   2. Back responds with a UserSession_Pydantic
#   3. Front sends post to /create a game
#   4. Back responds with a CreateGameResponse
#   5. Redirect to game

# To Play game
