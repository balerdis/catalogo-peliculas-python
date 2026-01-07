from fastapi import Request
from fastapi.responses import JSONResponse
from app.api.v1.schemas.generic import ErrorResponse
import logging

async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Fallback para cualquier error no controlado (500).
    """
    logging.exception("Unhandled server error", exc_info=exc)
    payload = ErrorResponse(
        success=False,
        message="Error interno del servidor",
        error_code="INTERNAL_SERVER_ERROR",
        details=None
    ).model_dump()
    return JSONResponse(status_code=500, content=payload)