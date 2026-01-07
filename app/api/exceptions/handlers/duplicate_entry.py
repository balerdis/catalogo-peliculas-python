# app/api/exceptions/handlers/duplicate_entry.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions.domain.duplicate_entry import DuplicateEntityError

async def duplicate_entity_exception_handler(
    request: Request,
    exc: DuplicateEntityError,
):
    return JSONResponse(
        status_code=409,
        content={
            "status": "error",
            "message": f"{exc.entity} already exists",
            "errors": [
                {
                    "field": exc.field,
                    "value": exc.value,
                    "message": str(exc)
                }
            ],
            "data": None
        },
    )