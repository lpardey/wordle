from passlib.context import CryptContext
from wordle_api.models import User
from wordle_api.config.settings import get_settings

SETTINGS = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(Exception):
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> User:
    user = await User.get_or_none(username=username)
    if user is None or not verify_password(password, user.password):
        raise AuthException()
    return user
