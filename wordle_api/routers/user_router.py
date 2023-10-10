from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from wordle_api.schemas.user_schemas import SignUpRequest, SignUpResponse, LoginRequest
from wordle_api.auth.utils import AuthException, authenticate_user, get_password_hash
from wordle_api.models import User, UserSession, User_Pydantic, UserSession_Pydantic

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/get", response_model=User_Pydantic)
async def get_user(username: str):
    user_query = await User.get_or_none(username=username)
    if user_query is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Username not found")
    user = await User_Pydantic.from_tortoise_orm(user_query)
    return user


@router.post("/create")
async def create_user(request: SignUpRequest) -> SignUpResponse:
    if await User.exists(username=request.username):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Username unavailable")
    try:
        raw_password = request.password.get_secret_value()
        hashed_password = get_password_hash(raw_password)
        user = await User.create(username=request.username, password=hashed_password)
        return SignUpResponse(user_id=user.id)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login", response_model=UserSession_Pydantic)
async def login(request: LoginRequest):
    try:
        raw_password = request.password.get_secret_value()
        user = await authenticate_user(request.username, raw_password)
        token = "auth token"
        session = await UserSession.create(user_id=user.id, token=token)
        return await UserSession_Pydantic.from_tortoise_orm(session)
    except AuthException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
