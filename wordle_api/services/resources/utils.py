# Dependencies
from passlib.context import CryptContext

# From apps
from wordle_api.config.settings import get_settings
from wordle_api.models import User

SETTINGS = get_settings()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(Exception):
    pass


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


async def authenticate_user(username: str, password: str) -> User:
    user = await User.get_or_none(username=username)
    if user is None or not verify_password(password, user.password_hash):
        raise AuthException
    return user
