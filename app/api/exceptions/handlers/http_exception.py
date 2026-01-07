from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.api.v1.schemas.generic import ErrorResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Formatea cualquier HTTPException (p.ej., 404 del GET-by-id) a nuestro JSON estándar.
    """
    # detail puede ser str o dict; nos aseguramos de devolver string legible
    msg = exc.detail if isinstance(exc.detail, str) else "Error en la solicitud"
    payload = ErrorResponse(
        success=False,
        message=msg,
        error_code=f"HTTP_{exc.status_code}",
        details=None
    ).model_dump()
    return JSONResponse(status_code=exc.status_code, content=payload)    