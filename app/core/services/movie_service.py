from app.api.v1.schemas.movies import MovieCreate, MovieUpdate
from app.core.services.base_service import BaseService
from app.core.services.dto.movie.search_dto import MovieSearchDTO
from app.core.services.dto.movie.report_filter_dto import ReportFilterDTO
from app.core.services.dto.movie.list_dto import MovieListDTO
from app.core.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork


class MovieService(BaseService):

    def create(self, data: MovieCreate):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.movies.create(data.model_dump())
        return result
    
    def search(self, 
               params: MovieSearchDTO
               ):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.movies.search(
                search=params.search,
                year_order_asc=params.year_order_asc,
                price_order_asc=params.price_order_asc,
                price_min=params.price_min,
                price_max=params.price_max,
                offset=params.offset,
                fetch=params.fetch
            )
        return result
    
    def get_all(self, 
                params: MovieListDTO
                ):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.movies.get_all_ordered(
                title_order_asc=params.title_order_asc,
                year_order_asc=params.year_order_asc,
                price_order_asc=params.price_order_asc,
                offset=params.offset,
                fetch=params.fetch
            )
        return result
    
    def get_reporte_resumen(
        self
        , filters: ReportFilterDTO
    ):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.movies.get_reporte_resumen(
                filters.genre, 
                filters.director, 
                filters.year_from, 
                filters.year_to            
            )
        return result
    
    def get_top_by_price(
        self
        , n: int = 5
    ):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.movies.get_top_by_price(n)
        return result
    
    def get_by_id_or_fail(self, id: int):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.movies.get_by_id_or_fail(id)
        return result
    
    def update(self, id: int, data: MovieUpdate):
        with SqlAlchemyUnitOfWork() as uow:
            movie = uow.movies.get_by_id_or_fail(id)

            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(movie, field, value)

            result = uow.movies.update(movie)
        return result
    
    def delete_by_id(self, id: int, confirm: bool = True):
        if not confirm:
            return

        with SqlAlchemyUnitOfWork() as uow:
            movie = uow.movies.get_by_id_or_fail(id)
            uow.movies.delete(movie)