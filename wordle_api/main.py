from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from wordle_api.routers.game import router as game_router
from wordle_api.routers.user import router as user_router
from wordle_api.config.settings import get_settings

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
    modules={"models": SETTINGS.MODELS},
    add_exception_handlers=True,
    generate_schemas=True,
)
