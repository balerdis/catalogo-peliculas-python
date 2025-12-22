from fastapi import APIRouter
from app.api.v1.schemas.movies import MovieCreate
from app.config.config import config
import logging


logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/hello")
def read_hello():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}

@router.post('/movie')
async def create_movie(request: MovieCreate):
    return {
        "success": True,
        "message": "Película creada exitosamente",
        "data": request.model_dump()
    }