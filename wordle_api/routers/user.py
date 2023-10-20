from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from wordle_api.schemas import LoginResponse, SignUpRequest, SignUpResponse
from wordle_api.services.authentication import create_access_token, get_current_active_user
from wordle_api.services.resources.utils import AuthException, get_password_hash, authenticate_user
from wordle_api.pydantic_models import User_Pydantic
from wordle_api.models import User, UserSession

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/get/me", response_model=User_Pydantic)
async def get_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await User_Pydantic.from_tortoise_orm(current_user)


# Admin
@router.get("/get", response_model=User_Pydantic)
async def get_any_user(username: str):
    user = await User.get_or_none(username=username)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with {username=} not found")
    return await User_Pydantic.from_tortoise_orm(user)


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


@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> LoginResponse:
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        access_token = create_access_token(data={"sub": user.username})
        session = await UserSession.create(access_token=access_token, user_id=user.id)
        return LoginResponse(
            session_id=session.id,
            user_id=user.id,
            access_token=access_token,
            token_type="bearer",
            session_creation_date=session.creation_date,
        )
    except AuthException:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
