from fastapi import FastAPI
from wordle_api.routers import game, player
from wordle_api.user.router import router as user_router
from wordle_api.auth.asdf import router as auth_router

app = FastAPI()
app.include_router(game.router)
app.include_router(player.router)
app.include_router(auth_router)
app.include_router(user_router)
