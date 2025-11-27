# src/repository/user_repository.py

from typing import Optional

from sqlmodel import Session, select

from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import get_password_hash  # ⬅️ IMPORTAR


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    result = session.exec(statement).first()
    return result


def create_user(session: Session, user_in: UserCreate) -> User:
    """
    Cria um novo usuário no banco com senha hasheada.
    """
    hashed = get_password_hash(user_in.password)
    user = User(username=user_in.username, password=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
