# app/api/exceptions/register.py
from app.api.exceptions.handlers.duplicate_entry import duplicate_entity_exception_handler
from app.api.exceptions.handlers.entity_not_found import entity_not_found_handler
from app.api.exceptions.handlers.http_exception import http_exception_handler
from app.api.exceptions.handlers.unhandled import unhandled_exception_handler
from app.core.exceptions.domain.duplicate_entry import DuplicateEntityError
from app.core.database.repositories.base_repository import EntityNotFoundError

from fastapi import FastAPI, HTTPException

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        EntityNotFoundError,
        entity_not_found_handler,
    )

    app.add_exception_handler(
        DuplicateEntityError,
        duplicate_entity_exception_handler,
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )