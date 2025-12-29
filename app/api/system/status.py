from fastapi import status, APIRouter, HTTPException
from time import time
from app.config.config import config
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["SYSTEM"])

@router.get("/status", status_code=status.HTTP_200_OK)
async def health():
    try:
        return {
            "application": {
                "name": config.APP_NAME,
                "version": config.APP_VERSION,
                "environment": config.ENVIRONMENT,
                "debug": config.DEBUG,
            },
            "runtime": {
                "uptime_seconds": int(time()),
            },
            "features": {
                "authentication": True,
                "database": True,
            }
        }
            
    except Exception as e:
        logger.exception("Error getting API status")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve API status"
        )   