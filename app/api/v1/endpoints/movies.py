from app.api.v1.schemas.movies import MovieCreate, MovieResponse, MovieUpdate, DeleteMovieResponse
from app.api.v1.schemas.generic import ApiResponse
from fastapi import status, APIRouter
from app.core.database.connection import db_connection
from app.core.database.repositories.movie_repository import MovieRepository
from sqlalchemy.orm import Session
from fastapi import Depends


from app.config.config import config
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/hello")
def read_hello():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}

@router.post("/", response_model=ApiResponse[MovieResponse])
def create_movie(
    request: MovieCreate,
    db: Session = Depends(db_connection.get_db),
):
    repo = MovieRepository(db)
    movie = repo.create(request.model_dump())

    return ApiResponse(
        status="success",
        message="Película creada correctamente",
        errors=[],
        data=MovieResponse.model_validate(movie)
    )

@router.get("/", response_model=ApiResponse[list[MovieResponse]])
def get_movies(
    db: Session = Depends(db_connection.get_db),
):
    repo = MovieRepository(db)
    movies = repo.get_all()
    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[MovieResponse.model_validate(m) for m in movies]
    )

@router.get("/{movie_id}", response_model=ApiResponse[MovieResponse])
def get_movie_by_id(
    movie_id: int,
    db: Session = Depends(db_connection.get_db),
):
    repo = MovieRepository(db)

    movie = repo.get_by_id_or_fail(movie_id)


    return ApiResponse(
        status="success",
        message="La consulta fue realizada exitosamente",
        errors=[],
        data=MovieResponse.model_validate(movie)
    )

@router.patch("/{movie_id}", response_model=ApiResponse[MovieResponse])
def update_movie_by_id(
    movie_id: int,
    request: MovieUpdate,
    db: Session = Depends(db_connection.get_db),
):
    repo = MovieRepository(db)

    movie = repo.get_by_id_or_fail(movie_id)
    update_data = request.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(movie, field, value)

    return ApiResponse(
        status="success",
        message="La consulta fue realizada exitosamente",
        errors=[],
        data=MovieResponse.model_validate(repo.update(movie))
    )

@router.delete(
        "/{movie_id}"
        , response_model=ApiResponse[DeleteMovieResponse]
        , status_code=status.HTTP_200_OK
)
def delete_movie_by_id(
    movie_id: int,
    db: Session = Depends(db_connection.get_db),
):
    
    repo = MovieRepository(db)    
    repo.delete_by_id(movie_id)

    return ApiResponse(
        status="success",
        message="Película eliminada correctamente",
        errors=[],
        data=DeleteMovieResponse(id=movie_id)
    )
