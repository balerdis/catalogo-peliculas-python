from fastapi import status, APIRouter, HTTPException, Depends
from app.api.v1.schemas.status.responses import StatusResponse, ApplicationStatus, RuntimeStatus, FeaturesStatus
from app.core.database.connection import db_connection
from sqlalchemy.orm import Session
from sqlalchemy import text
from time import time
from app.config.config import config
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["SYSTEM"])

@router.get("/status", status_code=status.HTTP_200_OK)
async def health(
    db: Session = Depends(db_connection.get_db)
):
    """La idea de este service es que muestre estados intermedios del status, y a la vez
    muestre que devuelve status_code = 200

    Args:
        db (Session, optional): session de la base de datos. Defaults to Depends(db_connection.get_db).

    Returns:
        StatusResponse: estructura de status response
    """
    db_status = "up"

    try:
        db.execute(text("SELECT 1"), execution_options={"timeout": 2})
    except Exception:
        db_status = "down"

    overall_status = "ok"
    if db_status == "down":
        overall_status = "degraded"

    return StatusResponse(
        status=overall_status,
        application=ApplicationStatus(
            name=config.APP_NAME,
            version=config.APP_VERSION,
            environment=config.ENVIRONMENT,
            debug=config.DEBUG,
        ),
        runtime=RuntimeStatus(
            uptime_seconds=int(time()),
        ),
        features=FeaturesStatus(
            authentication=True,
            database=(db_status == "up"),
        ),
    )