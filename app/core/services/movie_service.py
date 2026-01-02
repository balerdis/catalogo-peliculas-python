from app.api.v1.schemas.movies import MovieCreate, MovieUpdate
from app.core.services.base_service import BaseService
from app.core.services.dto.movie.search_dto import MovieSearchDTO
from app.core.services.dto.movie.report_filter_dto import ReportFilterDTO
from app.core.services.dto.movie.list_dto import MovieListDTO
from app.core.database.repositories.movie_repository import MovieRepository


class MovieService(BaseService):

    def __init__(self, repository: MovieRepository):
        super().__init__(repository)
        self.repository: MovieRepository = repository

    def create(self, data: MovieCreate):
        return self.repository.create(data.model_dump())
    
    def search(self, 
               params: MovieSearchDTO
               ):
        return self.repository.search(
            search=params.search,
            year_order_asc=params.year_order_asc,
            price_order_asc=params.price_order_asc,
            price_min=params.price_min,
            price_max=params.price_max,
            offset=params.offset,
            fetch=params.fetch
        )
    
    def get_all(self, 
                params: MovieListDTO
                ):
        return self.repository.get_all_ordered(
            title_order_asc=params.title_order_asc,
            year_order_asc=params.year_order_asc,
            price_order_asc=params.price_order_asc,
            offset=params.offset,
            fetch=params.fetch
        )
    
    def get_reporte_resumen(
        self
        , filters: ReportFilterDTO
    ):
        return self.repository.get_reporte_resumen(
            filters.genre, 
            filters.director, 
            filters.year_from, 
            filters.year_to
        )
    
    def get_top_by_price(
        self
        , n: int = 5
    ):
        return self.repository.get_top_by_price(n)
    
    def get_by_id_or_fail(self, id: int):
        return self.repository.get_by_id_or_fail(id)
    
    def update(self, id: int, data: MovieUpdate):
        movie = self.repository.get_by_id_or_fail(id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(movie, field, value)

        return self.repository.update(movie)
    
    def delete_by_id(self, id: int, confirm: bool = True):
        return self.repository.delete_by_id(id, confirm)