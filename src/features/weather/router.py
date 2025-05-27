import uuid

import httpx
from fastapi import APIRouter, Response, Request
from sqlalchemy import select

from src.database import async_session_maker
from src.features.history.models import History
from src.features.history.dao import HistoryDao
from src.features.weather.schemas import ListCitySuggestion
from src.exceptions import APIIntegrationError
from src.features.weather.service import get


router = APIRouter(
    prefix='/weather',
    tags=['Погода'],
)


def generate_uuid():
    return str(uuid.uuid4())


@router.get("/api/suggestions")
async def get_suggestions(q: str = None) -> ListCitySuggestion:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": q, "count": 5, "language": "ru",
            },
            timeout=5.0
        )
        if response.status_code == 200:
            return response.json()
        raise APIIntegrationError(
            f'Слишком долгое ожидание от сервера'
        )


@router.get('/')
async def get_weather(request: Request, response: Response, city: str):
    weather_forecast = await get(city)

    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = f"{generate_uuid()}"
        response.set_cookie("user_id", user_id, max_age=2865)

    await HistoryDao.add(user_id=user_id, city=city)

    return weather_forecast


@router.get("/api/last_city")
async def get_last_city(request: Request):
    async with async_session_maker() as session:
        user_id = request.cookies.get("user_id")
        if not user_id:
            return {"last_city": None}

        result = await session.execute(
            select(History)
            .where(History.user_id == user_id)
            .order_by(History.created_at.desc())
            .limit(1)
        )
        last_search = result.scalars().first()

    return {"last_city": last_search.city if last_search else None}