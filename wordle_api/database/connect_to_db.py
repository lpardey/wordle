from tortoise import Tortoise


async def connect_to_db() -> None:
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["wordle_api.models"]},
    )
