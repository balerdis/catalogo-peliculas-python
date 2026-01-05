from tkinter import NO
from app.config.config import config
from app.core.services.base_service import BaseService
from app.api.v1.schemas.genres.create import GenreCreate
from app.core.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork

class GenreService(BaseService):
    def get_all(self):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.genres.get_all()
        return result
    
    def create(self, data: GenreCreate):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.genres.create(data.model_dump)        
        return result
    def get_by_id_or_fail(self, id: int):
        with SqlAlchemyUnitOfWork() as uow:
            result = uow.genres.get_by_id_or_fail(id)
        return result
    
    def update(self, id: int, data: GenreCreate):
        with SqlAlchemyUnitOfWork() as uow:
            genre = uow.genres.get_by_id_or_fail(id)
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(genre, field, value)
            result = uow.genres.update(genre)
        return result
    

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
            uow.genres.get_by_id_or_fail(id)
            movies = uow.movies.get_by_genre_id(id)
            for movie in movies:
                movie.genre_id = genre_no_identified.id
                if confirm: uow.movies.update(movie)
            uow.genres.delete_by_id(id, confirm)
    