# Standard Library
import logging
from datetime import datetime, timedelta
from typing import Annotated

# Dependencies
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# From apps
from api.v1.settings import get_settings
from api.v1.user.models import User

logger = logging.getLogger("Auth")

SETTINGS = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expires_delta = expires_delta if expires_delta is not None else timedelta(minutes=SETTINGS.ACCESS_TOKEN_LIFETIME)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTINGS.SECRET_KEY, algorithm=SETTINGS.TOKEN_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.TOKEN_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something unexpected happened")
    user = await User.get_or_none(username=username)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with {username=} not found")
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
