from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite://db.sqlite3"
    SECRET_KEY: str = "c2be1062540cd526c982764243e6ab5247fb4d638d4a4f088ce904d4fda63b45"  # openssl rand -hex 32
    APP_NAME: str = "Wordlematic"
    REGISTRATION_TOKEN_LIFETIME: int = 120  # TODO
    ACCESS_TOKEN_LIFETIME: int = 30
    TOKEN_ALGORITHM: str = "HS256"
    SMTP_SERVER: str = "localhost:25"
    MAIL_SENDER: str = "noreply@example.com"  # TODO
    API_PREFIX: str = "/"
    HOST: str = "localhost"
    PORT: int = 8000
    BASE_URL: str = f"{HOST}:{PORT}/"
    MODELS: list[str] = ["wordle_api.models", "wordle_api.pydantic_models"]

    class Config:
        case_sensitive: bool = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
