from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.features.weather.router import router as weather_router

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(weather_router)