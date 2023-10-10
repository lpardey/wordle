from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from wordle_api.schemas.user_schemas import SignUpRequest, LoginRequest, LoginResponse, SignUpResponse
from wordle_api.auth.utils import AuthException, authenticate_user, get_password_hash
from wordle_api.models import User, UserSession, User_Pydantic


router = APIRouter(prefix="/account", tags=["Account"])


LOGIN_FAILED = HTTPException(status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")


@router.get("/get")
async def get_user(username: str) -> User_Pydantic:
    user_query = await User.get_or_none(username=username)
    if user_query is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Username '{username}' not found")
    user = await User_Pydantic.from_tortoise_orm(user_query)
    return user


@router.post("/create")
async def create_user(request: SignUpRequest) -> SignUpResponse:
    if await User.exists(username=request.username):
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"Username '{request.username}' is unavailable")
    try:
        hashed_password = get_password_hash(request.password.get_secret_value())
        user = await User.create(username=request.username, password=hashed_password)
        return SignUpResponse(user_id=user.id)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login")
async def login(request: LoginRequest) -> LoginResponse:
    try:
        user = await authenticate_user(request.username, request.password)
        token = "auth token"
        session = await UserSession.create(user_id=user.id, token=token)
        return LoginResponse(
            session_id=session.id,
            user_id=session.user_id,  # DB-backing field: for some reason tortoise appends '_id' to FK fields by default.
            token=token,
            session_creation_date=session.session_creation_date,
        )
        # return await UserSession_Pydantic.from_tortoise_orm(session)  # TODO: Relations & Early-init isn't happening
    except AuthException:
        raise LOGIN_FAILED
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
