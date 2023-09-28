from functools import wraps

from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi import status
from .store import SessionStore, SessionStoreDict
from datetime import datetime


def authorized_endpoint(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        token: str | None = request.headers.get("token")
        # comprobar que la request tenga un token
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        # comprobar que el token este asociado a una sesion activa
        session_store: SessionStore = SessionStoreDict.get_instance()
        user_session = session_store.get_session(token)
        if user_session.expiration_date < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper
