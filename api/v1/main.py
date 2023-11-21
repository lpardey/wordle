# Dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

# From apps
from api.v1.game.routers.game import router as game_router
from api.v1.user.routers.user import router as user_router

# Local imports
from .settings import get_settings

SETTINGS = get_settings()

app = FastAPI(title=SETTINGS.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

app.include_router(game_router)

register_tortoise(
    app,
    db_url=SETTINGS.DATABASE_URL,
    modules={"models": SETTINGS.DATABASE_MODELS},
    add_exception_handlers=True,
    generate_schemas=True,
)
