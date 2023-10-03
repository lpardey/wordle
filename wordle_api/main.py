from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from wordle_api.routers import game
from wordle_api.user.router import router as user_router
# from wordle_api.auth.asdf import router as auth_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(game.router)
# app.include_router(auth_router)
