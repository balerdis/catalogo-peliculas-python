from fastapi import APIRouter, FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.middleware.auth_middleware import AuthMiddleware
from app.api.system.router import router as system_router
from app.core.database.connection import db_connection
from app.api.v1.endpoints.movies import router as api_router_movies
from app.api.v1.endpoints.genres import router as api_router_genres
from app.api.v1.endpoints.users import router as api_router_users
from app.api.exceptions.register import register_exception_handlers

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

    register_exception_handlers(app)    
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

