from passlib.context import CryptContext


from wordle_api.user.models import User

from wordle_api.user.store import UserStore, UserStoreDict


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(Exception):
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> User:
    user_store: UserStore = UserStoreDict.get_instance()
    user = user_store.get_user(username)
    if not user or not verify_password(password, user.password):
        raise AuthException()
    return user
