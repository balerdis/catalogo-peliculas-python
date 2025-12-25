from app.api.v1.schemas.movies import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    ReportFilter,
    MoviesReportSummary,
    DeleteMovieResponse,
)
from app.api.v1.schemas.generic import ApiResponse
from fastapi import status, APIRouter
from app.core.database.connection import db_connection
from app.core.database.repositories.movie_repository import MovieRepository
from sqlalchemy.orm import Session
from fastapi import Depends


router = APIRouter()

@router.post("/"
             , response_model=ApiResponse[MovieResponse]
             , status_code=status.HTTP_201_CREATED
             , description="Crea una nueva película"
             )
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


@router.get("/hello"
            , status_code=status.HTTP_200_OK
            , description="Endpoint de prueba"
            )
def read_hello():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}


@router.get("/buscar"
            , response_model=ApiResponse[list[MovieResponse]]
            , status_code=status.HTTP_200_OK
            , description="Búsqueda por titulo, director o genero total o parcial y por rango de precio, paginado, y orden por año o precio")
def search_movies(
    search: str | None = None,
    year_order_asc: bool = False,
    price_order_asc: bool = False,
    price_min: float = 0.0,
    price_max: float | None = None,
    offset: int = 0,
    fetch: int = 100,
    db: Session = Depends(db_connection.get_db),
):
    repo = MovieRepository(db)
    movies = repo.search(
        search=search,
        year_order_asc=year_order_asc,
        price_order_asc=price_order_asc,
        price_min=price_min,
        price_max=price_max,
        offset=offset,
        fetch=fetch
        )
    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[MovieResponse.model_validate(m) for m in movies]
    )


@router.get("/"
            , response_model=ApiResponse[list[MovieResponse]]
            , status_code=status.HTTP_200_OK
            , description="Listado de todas las películas"
            )
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


@router.get("/reporte_resumen"
            , response_model=ApiResponse[MoviesReportSummary]
            , status_code=status.HTTP_200_OK
            , description="Reporte. Conteos y valor del inventario, filtros parciales por genero, director y año"
            )
def get_reporte_resumen(
    filters: ReportFilter = Depends(),
    db: Session = Depends(db_connection.get_db)
):
    repo = MovieRepository(db)

    reporte = repo.get_reporte_resumen(
        genre=filters.genre,
        director=filters.director,
        year_from=filters.year_from,
        year_to=filters.year_to,
    )

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


@router.get("/top_por_precio"
            , response_model=ApiResponse[list[MovieResponse]]
            , status_code=status.HTTP_200_OK
            , description="Devuelve el top de las peliculas por precio")
def get_top_by_price(
    db: Session = Depends(db_connection.get_db),
    n: int = 5
):
    repo = MovieRepository(db)

    movies = repo.get_top_by_price(n)

    return ApiResponse(
        status="success",
        message="La consulta fue realizada exitosamente",
        errors=[],
        data=movies
    )


@router.get("/{movie_id}"
            , response_model=ApiResponse[MovieResponse]
            , status_code=status.HTTP_200_OK
            , description="Búsqueda por id"
            )
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
    repo = MovieRepository(db)    
    repo.delete_by_id(movie_id, confirm)

    return ApiResponse(
        status="success",
        message="Película eliminada correctamente",
        errors=[],
        data=DeleteMovieResponse(id=movie_id)
    )
