from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.database.repositories.base_repository import EntityNotFoundError
from fastapi import status
from app.api.v1.schemas.generic import ErrorResponse

async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    msg = f"Entidad no encontrada: {str(exc)}"
    payload = ErrorResponse(
        success=False,
        message=msg,
        error_code="ENTITY_NOT_FOUND",
        details=None
    ).model_dump()
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=payload)