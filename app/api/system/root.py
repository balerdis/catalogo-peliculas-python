from fastapi import APIRouter
from app.config.config import config
from app.api.v1.schemas.generic import ApiResponse

router = APIRouter(tags=["SYSTEM"])


@router.get("/", response_model=ApiResponse)
async def root():
    return ApiResponse(
        status="success",
        message=f"{config.APP_NAME} v{config.APP_VERSION} - API funcionando correctamente",
        errors=[],
        data={
            "version": config.APP_VERSION,
            "docs_url": "/docs" if config.DEBUG else "Disabled in production",
            "endpoints": {
                "movies_queries": "/api/v1/movies/",
                "genres_queries": "/api/v1/genres/",
                "health": "/health",
                "status": "/status"
            }
        }
    )
