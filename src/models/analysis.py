# src/models/analysis.py
from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from .project import Project


class AnalysisHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(index=True)
    # NOVO: projeto dono dessa análise (pode ser nulo)
    project_id: Optional[int] = Field(default=None, index=True)

    topic: str
    platform: str
    mode: str

    result_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    project: Optional[Project] = Relationship(back_populates="analyses")
