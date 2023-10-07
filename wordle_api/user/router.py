from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

# from wordle_api.user.auth import authorized_endpoint
# from .store import (
#     SessionStore,
#     SessionStoreDict,
#     StoreExceptionAlreadyInUse,
#     StoreExceptionNotFound,
#     StoreExceptionUnexpected,
#     UserStoreDict,
#     UserStore,
# )
from .schemas import SignUpRequest, LoginRequest, LoginResponse, SignUpResponse
from wordle_api.auth.utils import AuthException, authenticate_user, get_password_hash
from wordle_api.models.user import User, User_Pydantic
from wordle_api.models.user_session import UserSession, UserSession_Pydantic

router = APIRouter(prefix="/account", tags=["Account"])


LOGIN_FAILED = HTTPException(status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")


# @router.put("/update/{user_id}")
# # @authorized_endpoint
# def update_user(request: Request, user_id: int, update_request: UpdateRequest) -> None:
#     try:
#         user_store: UserStore = UserStoreDict.get_instance()
#         user = User(id=user_id, username=update_request.username, password=update_request.password)
#         user_store.update_user(user)

#     except StoreExceptionAlreadyInUse as e:
#         raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))

#     except StoreExceptionUnexpected as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# @router.delete("/delete/{user_id}")
# # @authorized_endpoint
# def delete_user(request: Request, user_id: int) -> None:
#     try:
#         user_store: UserStore = UserStoreDict.get_instance()
#         user_store.delete_user(user_id)

#     except StoreExceptionNotFound as e:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

#     except StoreExceptionUnexpected as e:
#         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


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
        hashed_password = get_password_hash(request.password)
        user = await User.create(username=request.username, password=hashed_password)
        return SignUpResponse(user_id=user.id)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login")
async def login(request: LoginRequest):
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
        # return await UserSession_Pydantic.from_tortoise_orm(session) # TODO: Relations & Early-init isn't happening
    except AuthException:
        raise LOGIN_FAILED
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
