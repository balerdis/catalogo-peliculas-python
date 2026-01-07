from app.api.v1.schemas.movies import MovieCreate, MovieUpdate, MovieResponse, MoviesReportSummary
from app.api.v1.schemas.genres.responses import GenreResponse
from app.core.services.base_service import BaseService
from app.core.services.dto.movie.search_dto import MovieSearchDTO
from app.core.services.dto.movie.report_filter_dto import ReportFilterDTO
from app.core.services.dto.movie.list_dto import MovieListDTO
from app.core.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork


class MovieService(BaseService):

    def create(self, data: MovieCreate) -> MovieResponse:
        with SqlAlchemyUnitOfWork() as uow:
            movie = uow.movies.create(data.model_dump())
            return self._map_movie_to_response(movie)
            
    
    def search(self, 
               params: MovieSearchDTO
               ) -> list[MovieResponse]:
        with SqlAlchemyUnitOfWork() as uow:
            movies = uow.movies.search(
                search=params.search,
                year_order_asc=params.year_order_asc,
                price_order_asc=params.price_order_asc,
                price_min=params.price_min,
                price_max=params.price_max,
                offset=params.offset,
                fetch=params.fetch
            )
            return [self._map_movie_to_response(m) for m in movies]
    
    def get_all(self, 
                params: MovieListDTO
                ) -> list[MovieResponse]:
        with SqlAlchemyUnitOfWork() as uow:
            movies = uow.movies.get_all_ordered(
                title_order_asc=params.title_order_asc,
                year_order_asc=params.year_order_asc,
                price_order_asc=params.price_order_asc,
                offset=params.offset,
                fetch=params.fetch
            )
            return [self._map_movie_to_response(m) for m in movies]
    
    def get_reporte_resumen(
        self
        , filters: ReportFilterDTO
    ) -> MoviesReportSummary:
        with SqlAlchemyUnitOfWork() as uow:
            reporte = uow.movies.get_reporte_resumen(
                filters.genre, 
                filters.director, 
                filters.year_from, 
                filters.year_to            
            )
            return MoviesReportSummary(
                total_movies=reporte.total_movies,
                total_units=reporte.total_units,
                total_price=float(reporte.total_price or 0),
            )
    
    def get_top_by_price(
        self
        , n: int = 5
    ) -> list[MovieResponse]:
        with SqlAlchemyUnitOfWork() as uow:
            movies = uow.movies.get_top_by_price(n)
            return [self._map_movie_to_response(m) for m in movies]
    
    def get_by_id_or_fail(self, id: int) -> MovieResponse:
        with SqlAlchemyUnitOfWork() as uow:
            m = uow.movies.get_by_id_or_fail(id)

            return self._map_movie_to_response(m)
    
    def update(self, id: int, data: MovieUpdate) -> MovieResponse:
        with SqlAlchemyUnitOfWork() as uow:
            movie = uow.movies.get_by_id_or_fail(id)

            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(movie, field, value)

            movie = uow.movies.update(movie)
            return self._map_movie_to_response(movie)
                
            
    
    def delete_by_id(self, id: int, confirm: bool = True) -> None:
        if not confirm:
            return

        with SqlAlchemyUnitOfWork() as uow:
            movie = uow.movies.get_by_id_or_fail(id)
            uow.movies.delete(movie)


    def _map_movie_to_response(self, m) -> MovieResponse:
        return MovieResponse(
            id=m.id,
            title=m.title,
            director=m.director,
            year=m.year,
            price=m.price,
            duration=m.duration,
            rating=m.rating,
            description=m.description,
            genre=(
                    GenreResponse(
                        id=m.genre.id,
                        name=m.genre.name
                    ) if m.genre else None
                )
        )