from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from wordle_api.schemas import LoginResponse, SignUpRequest
from wordle_api.schemas.user import CreateUserResponse
from wordle_api.services.authentication import create_access_token, get_current_active_user
from wordle_api.services.resources.utils import AuthException, get_password_hash, authenticate_user
from wordle_api.pydantic_models import User_Pydantic
from wordle_api.models import User, UserSession
import logging

logger = logging.getLogger("User")

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/me", response_model=User_Pydantic)
async def get_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await User_Pydantic.from_tortoise_orm(current_user)


# Admin
@router.get("/{username}", response_model=User_Pydantic)
async def get_any_user(username: Annotated[str, Path(title="Username")]):
    user = await User.get_or_none(username=username)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with {username=} not found")
    return await User_Pydantic.from_tortoise_orm(user)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(request: SignUpRequest) -> CreateUserResponse:
    if await User.exists(username=request.username):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Username unavailable")
    try:
        password = request.password.get_secret_value()
        password_hash = get_password_hash(password)
        user = await User.create(username=request.username, password_hash=password_hash)
        return CreateUserResponse(
            user_id=user.id,
            username=user.username,
            disabled=user.disabled,
            creation_date=user.creation_date,
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> LoginResponse:
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        token = create_access_token(data={"sub": user.username})
        session = await UserSession.create(access_token=token, user_id=user.id)
        return LoginResponse(
            session_id=session.id,
            user_id=user.id,
            access_token=token,
            token_type="bearer",
            session_creation_date=session.creation_date,
        )
    except AuthException:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
