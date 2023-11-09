# Dependencies
from tortoise import Tortoise, run_async

# From apps
from api.v1.main import MODELS
from api.v1.settings import get_settings

SETTINGS = get_settings()


async def purge_db():
    await Tortoise.init(
        db_url=SETTINGS.DATABASE_URL,
        modules={"models": MODELS},
    )
    await Tortoise._drop_databases()


if __name__ == "__main__":
    run_async(purge_db())
