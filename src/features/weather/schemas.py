from typing import List

from pydantic import BaseModel


class CitySuggestion(BaseModel):
    name: str
    latitude: float
    longitude: float


class ListCitySuggestion(BaseModel):
    results: List[CitySuggestion] | None = []
    generationtime_ms: float | None = None