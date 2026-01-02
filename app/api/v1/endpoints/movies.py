from app.api.v1.schemas.movies import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MoviesReportSummary,
    DeleteMovieResponse,
)

from app.api.v1.schemas.generic import ApiResponse
from fastapi import status, APIRouter
from app.core.database.connection import db_connection
from app.core.database.repositories.movie_repository import MovieRepository
from app.core.services.movie_service import MovieService
from app.core.services.dto.movie.search_dto import MovieSearchDTO
from app.core.services.dto.movie.list_dto import MovieListDTO
from app.core.services.dto.movie.report_filter_dto import ReportFilterDTO
from sqlalchemy.orm import Session
from fastapi import Depends


router = APIRouter()
# ###################CREATE MOVIE###################
@router.post("/"
             , response_model=ApiResponse[MovieResponse]
             , status_code=status.HTTP_201_CREATED
             , description="Crea una nueva película"
             )
def create_movie(
    request: MovieCreate,
    db: Session = Depends(db_connection.get_db),
):
    service = MovieService(MovieRepository(db))
    movie = service.create(request)

    return ApiResponse(
        status="success",
        message="Película creada correctamente",
        errors=[],
        data=MovieResponse.model_validate(movie)
    )

# ###################TEST ENDPOINT###################
@router.get("/hello"
            , status_code=status.HTTP_200_OK
            , description="Endpoint de prueba"
            )
def read_hello():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}

# ###################SEARCH MOVIE###################
@router.get("/buscar"
            , response_model=ApiResponse[list[MovieResponse]]
            , status_code=status.HTTP_200_OK
            , description="Búsqueda por titulo, director o genero total o parcial y por rango de precio, paginado, y orden por año o precio")
def search_movies(
    params: MovieSearchDTO = Depends(),
    db: Session = Depends(db_connection.get_db),
):
    service = MovieService(MovieRepository(db))
    movies = service.search(params)

    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[MovieResponse.model_validate(m) for m in movies]
    )

# #####################GET ALL MOVIES################
@router.get("/"
            , response_model=ApiResponse[list[MovieResponse]]
            , status_code=status.HTTP_200_OK
            , description="Listado de todas las películas"
            )
def get_movies(
    params: MovieListDTO = Depends(),
    db: Session = Depends(db_connection.get_db),
):
    service = MovieService(MovieRepository(db))

    movies = service.get_all(params)
    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[MovieResponse.model_validate(m) for m in movies]
    )

# #####################GET REPORT RESUMEN################
@router.get("/reporte_resumen"
            , response_model=ApiResponse[MoviesReportSummary]
            , status_code=status.HTTP_200_OK
            , description="Reporte. Conteos y valor del inventario, filtros parciales por genero, director y año"
            )
def get_reporte_resumen(
    filters: ReportFilterDTO = Depends(),
    db: Session = Depends(db_connection.get_db)
):
    service = MovieService(MovieRepository(db))

    reporte = service.get_reporte_resumen(filters)

    summary = MoviesReportSummary(
        total_movies=reporte.total_movies,
        total_units=reporte.total_units,
        total_price=float(reporte.total_price or 0),
    )

    return ApiResponse(
        status="success",
        message="La consulta fue realizada exitosamente",
        errors=[],
        data=MoviesReportSummary.model_validate(summary)
    )

# #####################GET TOP POR PRECIO################
@router.get("/top_por_precio"
            , response_model=ApiResponse[list[MovieResponse]]
            , status_code=status.HTTP_200_OK
            , description="Devuelve el top de las peliculas por precio")
def get_top_by_price(
    db: Session = Depends(db_connection.get_db),
    n: int = 5
):
    service = MovieService(MovieRepository(db))
    movies = service.get_top_by_price(n)

    return ApiResponse(
        status="success",
        message="La consulta fue realizada exitosamente",
        errors=[],
        data=[MovieResponse.model_validate(m) for m in movies]
    )

# #####################GET MOVIE BY ID################
@router.get("/{movie_id}"
            , response_model=ApiResponse[MovieResponse]
            , status_code=status.HTTP_200_OK
            , description="Búsqueda por id"
            )
def get_movie_by_id(
    movie_id: int,
    db: Session = Depends(db_connection.get_db),
):
    service = MovieService(MovieRepository(db))
    movie = service.get_by_id_or_fail(movie_id)


    return ApiResponse(
        status="success",
        message="La consulta fue realizada exitosamente",
        errors=[],
        data=MovieResponse.model_validate(movie)
    )

# #####################UPDATE MOVIE BY ID################
@router.patch("/{movie_id}"
              , response_model=ApiResponse[MovieResponse]
              , status_code=status.HTTP_200_OK
              , description="Actualiza una pelicula"
              )
def update_movie_by_id(
    movie_id: int,
    request: MovieUpdate,
    db: Session = Depends(db_connection.get_db),
):
    service = MovieService(MovieRepository(db))
    movie_updated = service.update(movie_id, request)

    return ApiResponse(
        status="success",
        message="La consulta fue realizada exitosamente",
        errors=[],
        data=MovieResponse.model_validate(movie_updated)
    )

# #####################DELETE MOVIE BY ID################
@router.delete(
        "/{movie_id}"
        , response_model=ApiResponse[DeleteMovieResponse]
        , status_code=status.HTTP_200_OK
        , description="Elimina una pelicula por id"
        )
def delete_movie_by_id(
    movie_id: int,
    confirm: bool = True,
    db: Session = Depends(db_connection.get_db),
) -> ApiResponse[DeleteMovieResponse]:
    """
    Elimina una pelicula, permite flag de confirmación util para dry-run

    Args:
        movie_id (int): id de la pelicula
        confirm (bool, optional): true si se desea realizar el borrado. Defaults to True.
        db (Session, optional): session de la base de datos. Defaults to Depends(db_connection.get_db).

    Returns:
        _type_: ApiResponse
    """
    service = MovieService(MovieRepository(db))
    service.get_by_id_or_fail(movie_id)
    service.delete_by_id(movie_id, confirm)

    return ApiResponse(
        status="success",
        message="Película eliminada correctamente",
        errors=[],
        data=DeleteMovieResponse(id=movie_id)
    )
