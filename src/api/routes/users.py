# src/api/routes/users.py

from fastapi import APIRouter, Depends
from src.schemas.user import UserRead
from src.api.routes.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: UserRead = Depends(get_current_user),
):
    """
    Retorna os dados do usuário autenticado.
    """
    return current_user
