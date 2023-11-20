# Standard Library
from functools import lru_cache

# Dependencies
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Wordlematic"
    DATABASE_URL: str = "sqlite://db.sqlite3"
    DATABASE_MODELS: list[str] = ["api.v1.game.models", "api.v1.user.models"]
    SECRET_KEY: str = "c2be1062540cd526c982764243e6ab5247fb4d638d4a4f088ce904d4fda63b45"  # openssl rand -hex 32
    REGISTRATION_TOKEN_LIFETIME: int = 120  # TODO
    ACCESS_TOKEN_LIFETIME: int = 30
    TOKEN_ALGORITHM: str = "HS256"
    SMTP_SERVER: str = "localhost:25"
    MAIL_SENDER: str = "noreply@example.com"  # TODO
    API_PREFIX: str = "/"
    HOST: str = "localhost"
    PORT: int = 8000
    BASE_URL: str = f"{HOST}:{PORT}/"

    class Config:
        case_sensitive: bool = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
