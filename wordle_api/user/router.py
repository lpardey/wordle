from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from wordle_api.user.auth import authorized_endpoint
from wordle_api.user.models import User
from .store import (
    SessionStore,
    SessionStoreDict,
    StoreExceptionAlreadyInUse,
    StoreExceptionNotFound,
    StoreExceptionUnexpected,
    UserStoreDict,
    UserStore,
)
from .schemas import SignUpRequest, LoginRequest, LoginResponse, UpdateRequest

router = APIRouter(prefix="/account", tags=["Account"])


LOGIN_FAILED = HTTPException(status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")


@router.get("/name_availability")
def is_user_available(username: str) -> None:
    user_store: UserStore = UserStoreDict.get_instance()
    if username in user_store.username_index:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"Username '{username}' is unavailable")


@router.put("/update/{user_id}")
@authorized_endpoint
def update_user(request: Request, user_id: int, update_request: UpdateRequest) -> None:
    try:
        user_store: UserStore = UserStoreDict.get_instance()
        user = User(id=user_id, username=update_request.username, password=update_request.password)
        user_store.update_user(user)

    except StoreExceptionAlreadyInUse as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))

    except StoreExceptionUnexpected as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete/{user_id}")
@authorized_endpoint
def delete_user(request: Request, user_id: int) -> None:
    try:
        user_store: UserStore = UserStoreDict.get_instance()
        user_store.delete_user(user_id)

    except StoreExceptionNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

    except StoreExceptionUnexpected as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/get")
def get_user(username: str) -> User:
    try:
        user_store: UserStore = UserStoreDict.get_instance()
        user = user_store.get_user(username)

    except StoreExceptionNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

    except StoreExceptionUnexpected as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return user


@router.post("/create")
def create_user(request: SignUpRequest) -> None:
    try:
        user_store: UserStore = UserStoreDict.get_instance()
        user_store.create_user(request.username, request.password)

    except StoreExceptionAlreadyInUse as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))

    except StoreExceptionUnexpected as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login")
def login(request: LoginRequest) -> LoginResponse:
    # si el usuario esta en el user store y la contraseña es correcta
    # crear un token y devolverlo
    # si no, dar un error http 404, not found
    try:
        user_store: UserStore = UserStoreDict.get_instance()
        user = user_store.get_user(request.username)
        if user.password == request.password:
            session_store: SessionStore = SessionStoreDict.get_instance()
            session_id = session_store.create_session(user.id)
            session = session_store.get_session_by_id(session_id)
            response = LoginResponse(token=session.token)
            return response
        raise LOGIN_FAILED

    except StoreExceptionNotFound:
        raise LOGIN_FAILED

    except StoreExceptionUnexpected as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
