from tortoise import Tortoise, run_async


async def purge_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["wordle_api.models", "wordle_api.pydantic_models"]},
    )
    await Tortoise._drop_databases()


if __name__ == "__main__":
    run_async(purge_db())
