from tortoise import Tortoise, run_async
from wordle_api.config.settings import get_settings

SETTINGS = get_settings()


async def purge_db():
    await Tortoise.init(
        db_url=SETTINGS.DATABASE_URL,
        modules={"models": SETTINGS.MODELS},
    )
    await Tortoise._drop_databases()


if __name__ == "__main__":
    run_async(purge_db())
