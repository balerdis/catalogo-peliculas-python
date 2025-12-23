from fastapi import APIRouter
from app.api.v1.schemas.movies import MovieCreate, MovieResponse
from app.core.database.connection import db_connection
from app.core.database.repositories.movie_repository import MovieRepository
from sqlalchemy.orm import Session
from fastapi import Depends


from app.config.config import config
import logging


logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/hello")
def read_hello():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}

@router.post("/", response_model=MovieResponse)
def create_movie(
    request: MovieCreate,
    db: Session = Depends(db_connection.get_db),
):
    repo = MovieRepository(db)
    return repo.create(request)