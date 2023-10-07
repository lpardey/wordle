from .database.initialize_db import initialize_db
from tortoise import Tortoise, run_async


async def main() -> None:
    await initialize_db()
    await Tortoise.generate_schemas()


async def drop_all_tables():
    await initialize_db()
    await Tortoise.generate_schemas()
    await Tortoise._drop_databases()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(main())
