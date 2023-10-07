from tortoise import Tortoise


async def initialize_db() -> None:
    Tortoise.init_models(["wordle_api.models"], "models")
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["wordle_api.models"]},
    )
