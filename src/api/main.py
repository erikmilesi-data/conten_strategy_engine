from fastapi import FastAPI

from src.utils.logger import get_logger

from src.api.routes.health import router as health_router
from src.api.routes.suggestions import router as suggestions_router
from src.api.routes.audience import router as audience_router
from src.api.routes.posting_time import router as posting_time_router
from src.api.routes.content_strategy import router as content_strategy_router

from src.api.routes.auth import router as auth_router

from src.database.db import init_db

logger = get_logger(__name__)


app = FastAPI(title="Content Strategy Engine")

init_db()

# Registrar rotas
app.include_router(health_router, prefix="/api")
app.include_router(suggestions_router, prefix="/api")
app.include_router(audience_router, prefix="/api")
app.include_router(posting_time_router, prefix="/api")
app.include_router(content_strategy_router, prefix="/api")
app.include_router(auth_router, prefix="/api")


@app.get("/")
def root():
    logger.info("Endpoint raiz acessado")
    return {"message": "Content Strategy Engine API funcionando!"}
