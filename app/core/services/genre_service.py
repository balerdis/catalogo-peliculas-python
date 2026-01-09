from app.config.config import config
from app.core.services.base_service import BaseService
from app.api.v1.schemas.genres.create import GenreCreate
from app.api.v1.schemas.genres.responses import GenreResponse
from app.core.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork

class GenreService(BaseService):
    def get_all(self) -> list[GenreResponse]:
        with SqlAlchemyUnitOfWork() as uow:
            genres = uow.genres.get_all()
            return [self._map_genre_to_response(g) for g in genres]
    
    def create(self, data: GenreCreate) -> GenreResponse:
        with SqlAlchemyUnitOfWork() as uow:
            genre = uow.genres.create(data.model_dump(), "name")        
            return self._map_genre_to_response(genre)
        
    def get_by_id_or_fail(self, id: int) -> GenreResponse:
        with SqlAlchemyUnitOfWork() as uow:
            genre = uow.genres.get_by_id_or_fail(id)
            return self._map_genre_to_response(genre)
    
    def update(self, id: int, data: GenreCreate) -> GenreResponse:
        with SqlAlchemyUnitOfWork() as uow:
            genre = uow.genres.get_by_id_or_fail(id)
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(genre, field, value)
            genre_updated = uow.genres.update(genre)
            return self._map_genre_to_response(genre_updated)
    

    def delete_by_id(self, id: int, confirm: bool = True) -> None:
        """
        Elimina un genero, como es una entidad relacionada con peliculas, se realizan algunas operaciones:
            1.- se revisa si existe una pelicula relacionada, en caso de existir las peliculas involucradas se setean al genero
            "sin identificar"
            2.- se elimina el genero
            TODO: en proximas versiones 
            1.- se hara soft delete indicando la fecha de borrado
            2.- se deberá adaptar la consulta de los generos que no se encuentren borrados
        Args:
            id (int): id del genero a eliminar
            confirm (bool, optional): para indicar si se desea realizar el borrado, si no, se emula un borrado. Defaults to True.

        Returns:
            _type_: No devuelve nada, no hace falta
        """

        with SqlAlchemyUnitOfWork() as uow:
            genre_no_identified = uow.genres.get_by_id_or_fail(config.GENRE_NOT_IDENTIFIED_ID)
            genre = uow.genres.get_by_id_or_fail(id)
            movies = uow.movies.get_by_genre_id(id)
            for movie in movies:
                movie.genre_id = genre_no_identified.id
                if confirm: uow.movies.update(movie)
            if confirm: uow.genres.delete_by_id(id, confirm)

    def _map_genre_to_response(self, g) -> GenreResponse:
        return GenreResponse(
            id=g.id,
            name=g.name
        )
    