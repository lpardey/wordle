# Standard Library
from datetime import UTC, datetime

# Dependencies
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.signals import post_save

# From apps
from api.v1.game.models import Game
from api.v1.game.services.resources.schemas import GameStatus


@post_save(Game)
async def update_game_finished_date(
    sender: type[Game],
    instance: Game,
    created: bool,
    using_db: BaseDBAsyncClient | None,
    update_fields: list[str],
) -> None:
    if instance.finished_date is None and await instance.status == GameStatus.FINISHED:
        await sender.filter(id=instance.id).update(finished_date=datetime.now(UTC))
