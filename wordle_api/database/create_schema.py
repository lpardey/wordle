from tortoise import Tortoise, run_async
from .connect_to_db import connect_to_db


async def main() -> None:
    await connect_to_db()
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(main())
