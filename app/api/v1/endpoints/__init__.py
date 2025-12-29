from app.api.v1.endpoints.genres import router as genres_router
from app.api.v1.endpoints.movies import router as movies_router

__all__ = [
    "genres_router",
    "movies_router",
]