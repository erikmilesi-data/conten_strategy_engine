# src/models/project.py
from __future__ import annotations

from typing import Optional, List
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class Project(SQLModel, table=True):
    """
    Projeto / Campanha de marketing do usuário.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # dono do projeto = id do usuário da tabela de auth
    owner_id: int = Field(index=True)

    name: str = Field(index=True, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # ligação com histórico de análises (vamos ajustar já já)
    analyses: List["AnalysisHistory"] = Relationship(back_populates="project")
