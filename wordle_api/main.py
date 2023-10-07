from wordle_api.database.initialize_db import initialize_db
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from wordle_api.game.router import router as game_router
from wordle_api.user.router import router as user_router

# from wordle_api.auth.asdf import router as auth_router

app = FastAPI(title="Wordlematic")
initialize_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(game_router)
# app.include_router(auth_router)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["wordle_api.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
