from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from wordle_api.user.models import User
from wordle_api.user.schemas import LoginResponse
from wordle_api.user.store import StoreExceptionNotFound, UserStore, UserStoreDict
from .utils import authenticate_user


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "c2be1062540cd526c982764243e6ab5247fb4d638d4a4f088ce904d4fda63b45"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # data tiene los datos que quieras poner en el token
    # se copia para no modificar el original
    to_encode = data.copy()
    # calculamos cuando queremos que expire el token
    expires_delta = expires_delta if expires_delta is not None else timedelta(minutes=15)
    expire = datetime.utcnow() + expires_delta
    # añadimos la expiración a los datos que queremos poner en el token
    to_encode.update({"exp": expire})
    # generamos el token con la información que queremos, la clave secreta que usa
    # nuestra aplicacion, y el algoritmo que queremos usar para generar el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user_store: UserStore = UserStoreDict.get_instance()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise CREDENTIALS_EXCEPTION

        user = user_store.get_user(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION

    except StoreExceptionNotFound:
        raise CREDENTIALS_EXCEPTION

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


@router.post("/token", response_model=LoginResponse)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> LoginResponse:
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except Exception:
        raise CREDENTIALS_EXCEPTION

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    response = LoginResponse(access_token=access_token, token_type="Bearer")
    return response


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]
