from time import time
from fastapi import APIRouter, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.api.v1.endpoints.movies import router as api_router_movies
from app.api.middleware.auth_middleware import AuthMiddleware
from app.core.database.connection import db_connection
from app.config.config import config
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, HTTPException, status

from .v1.schemas.generic import ApiResponse

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
    app.include_router(v1_router, prefix="/api/v1")

    @app.get("/", response_model=ApiResponse)
    async def root():
        return ApiResponse(
            success=True,
            message=f"{config.APP_NAME} v{config.APP_VERSION} - API funcionando correctamente",
            data={
                "version": config.APP_VERSION,
                "docs_url": "/docs" if config.DEBUG else "Disabled in production",
                "endpoints": {
                    "authentication": "/api/v1/auth/",
                    "rag_queries": "/api/v1/rag/",
                    "agent_queries": "/api/v1/agent/",
                    "health": "/health",
                    "status": "/status"
                }
            }
    )
    @app.get("/health")
    async def health_check():
        try:
            # Verificar conexión a base de datos
            with db_connection.get_session() as session:
                # Simple query para verificar conectividad
                result = session.execute(text("SELECT 1 as health_check")).fetchone()
                db_status = "healthy" if result and result[0] == 1 else "unhealthy"                
            
            health_data = {
                "status": "healthy",
                "timestamp": time(),
                "version": config.APP_VERSION,
                "database": db_status,
                "components": {
                    "api": "healthy",
                    "database": db_status,
                    "authentication": "healthy"
                }
            }
            
            return health_data
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unhealthy",
                    "timestamp": time(),
                    "version": config.APP_VERSION,
                    "error": str(e),
                    "components": {
                        "api": "healthy",
                        "database": "unhealthy",
                        "authentication": "unknown"
                    }
                }
            )
        
    @app.get("/status")
    async def api_status():
        try:
            total_users = 111
            active_users = 222

            
            return {
                "api_name": config.APP_NAME,
                "api_version": config.APP_VERSION,
                "database_status": "connected",
                "statistics": {
                    "total_users": total_users,
                    "active_users": active_users,
                },
                "configuration": {
                    "debug_mode": config.DEBUG,
                }
            }
                
        except Exception as e:
            logger.error(f"Error getting API status: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al obtener estado de la API"
            )          

          


    return app

app = create_app()

