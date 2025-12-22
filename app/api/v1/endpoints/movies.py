from fastapi import APIRouter
from app.config.config import config
import logging


logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/hello")
def read_hello():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}