import httpx
from fastapi import HTTPException

from src.features.weather.schemas import ListCitySuggestion


async def get(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city, "count": 1, "language": "ru",
            }
        )

        location = ListCitySuggestion(**response.json()).results

        if not location:
            raise HTTPException(
                status_code=404,
                detail=f"Город '{city}' не найден, проверьте правильность введенных данных"
            )

        location = location.pop()
        lat, lon = location.latitude, location.longitude

        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "hourly": "temperature_2m",
                "daily": "temperature_2m_max",
                "timezone": "auto",
                "forecast_days": 1
            }
        )

        return weather_response.json()