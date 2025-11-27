# src/api/routes/projects.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.database.sqlmodel_db import get_session

from src.schemas.project import ProjectCreate, ProjectRead
from src.services.projects import create_project, list_projects
from src.api.routes.auth import get_current_user  # já existe no seu projeto

from sqlmodel import Session, select

from src.models.project import Project
from src.api.routes.auth import get_current_user
from src.schemas.user import UserRead


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectRead])
def get_my_projects(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return list_projects(session, owner_id=current_user["id"])


@router.post("/", response_model=ProjectRead)
def create_project(
    payload: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return create_project(session, owner_id=current_user["id"], data=payload)
