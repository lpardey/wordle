# Dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

# From apps
from wordle_api.config.settings import get_settings
from wordle_api.routers.game import router as game_router
from wordle_api.routers.user import router as user_router

SETTINGS = get_settings()
MODELS = ["wordle_api.models", "wordle_api.pydantic_models"]
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
    modules={"models": MODELS},
    add_exception_handlers=True,
    generate_schemas=True,
)
