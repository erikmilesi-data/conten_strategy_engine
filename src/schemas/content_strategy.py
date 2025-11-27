# src/schemas/content_strategy.py

from typing import Any, List, Optional, Dict
from pydantic import BaseModel


class AudienceUser(BaseModel):
    age: int
    gender: str
    region: str


class ContentStrategyPayload(BaseModel):
    topic: str
    platform: str
    mode: str = "rich"
    users: Optional[List[AudienceUser]] = []


class ContentStrategyResponse(BaseModel):
    topic: str
    platform: str
    mode: str
    audience: Dict[str, Any]
    suggestions: Any
    best_times: Dict[str, Any]
