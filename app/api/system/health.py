from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from time import time
from app.api.v1.schemas.health.response import HealthResponse
from app.core.database.connection import db_connection
from app.config.config import config
from fastapi import Response
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["SYSTEM"])

@router.get(
        "/health", 
        response_model=HealthResponse,
        status_code=status.HTTP_200_OK
        )
async def health(
    response: Response,
    db: Session = Depends(db_connection.get_db)
    ):
    try:
        # Verificar conexión a base de datos y tira un timeout para por si la DB queda colgada
        db.execute(text("SELECT 1"), execution_options={"timeout": 2})
        

        return HealthResponse(
            status="ok",
            timestamp=int(time()),
            service=config.APP_NAME,
            version=config.APP_VERSION,
            components={
                "api": "up",
                "database": "up"
            }
        )
        
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return HealthResponse(
            status="error",
            timestamp=int(time()),
            service=config.APP_NAME,
            version=config.APP_VERSION,
            components={
                "api": "up",
                "database": "down"
            }
        )