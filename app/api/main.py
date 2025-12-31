from fastapi import APIRouter, FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.middleware.auth_middleware import AuthMiddleware
from app.api.system.router import router as system_router
from app.core.database.connection import db_connection
from app.core.database.repositories.base_repository import EntityNotFoundError
from app.api.v1.schemas.generic import ErrorResponse
from app.api.v1.endpoints.movies import router as api_router_movies
from app.api.v1.endpoints.genres import router as api_router_genres
from app.api.v1.endpoints.users import router as api_router_users

from app.config.config import config

import logging

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de STARTUP - se ejecuta antes de que la app reciba requests
    logger.info(f"Starting {config.APP_NAME}...")
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"API is ready !")
    
    # Aqui inicializar cualquier recurso que se necesite:
    # - Conexiones a base de datos
    # - Modelos de ML
    # - Caches
    # etc.
    
    yield  # Este yield separa startup de shutdown

    
    db_connection.close_connection()
    # Código de SHUTDOWN - se ejecuta cuando la app se cierra
    logger.info(f"Shutting down {config.APP_NAME}...")
    logger.info("Conexiones cerradas correctamente")

def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=config.APP_NAME,
        version=config.APP_VERSION,
        description=config.APP_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    @app.exception_handler(EntityNotFoundError)
    def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
        msg = f"Entidad no encontrada: {str(exc)}"
        payload = ErrorResponse(
            success=False,
            message=msg,
            error_code="ENTITY_NOT_FOUND",
            details=None
        ).model_dump()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=payload)
                            
    @app.exception_handler(HTTPException)
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

    @app.exception_handler(Exception)
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
    
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=config.APP_NAME,
            version=config.APP_VERSION,
            description=config.APP_DESCRIPTION,
            routes=app.routes,
        )

        app.openapi_schema = openapi_schema
        return app.openapi_schema        
    
    app.openapi = custom_openapi

    excluded_paths = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/health",
        "/favicon.ico",
    ]      

    protected_paths = []

    app.add_middleware(
        AuthMiddleware,
        excluded_paths=excluded_paths,
        protected_paths=protected_paths  
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )    

    logger.info("Auth Middleware configurated")

    v1_router = APIRouter()
    v1_router.include_router(api_router_movies, tags=["MOVIES"], prefix="/movies")
    v1_router.include_router(api_router_genres, tags=["GENRES"], prefix="/genres")
    v1_router.include_router(api_router_users, tags=["USERS"], prefix="/users")

    app.include_router(system_router)
    app.include_router(v1_router, prefix="/api/v1")

    logger.info("Routers configurated")


    return app

app = create_app()

