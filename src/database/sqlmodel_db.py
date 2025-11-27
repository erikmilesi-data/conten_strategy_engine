# src/database/sqlmodel_db.py

from typing import Generator

from sqlmodel import SQLModel, create_engine, Session

# 👉 Banco específico para os recursos que usarem SQLModel (ex: projetos/campanhas)
DATABASE_URL = "sqlite:///./content_strategy_sqlmodel.db"

# Para SQLite, geralmente é bom habilitar check_same_thread=False
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependência para injeção de sessão do SQLModel (FastAPI Depends).
    """
    with Session(engine) as session:
        yield session


def init_db_sqlmodel() -> None:
    """
    Inicializa as tabelas do SQLModel.
    No momento, se não houver modelos declarados, isso só garante que o
    metadata está pronto. Quando criarmos os modelos (Project, Campaign, etc.),
    eles serão criados aqui.
    """
    SQLModel.metadata.create_all(engine)
