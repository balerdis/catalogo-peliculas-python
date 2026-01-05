from app.config.config import config
from app.core.services.base_service import BaseService
from app.core.database.repositories.genre_repository import GenreRepository
from app.core.database.repositories.movie_repository import MovieRepository
from app.api.v1.schemas.genres.create import GenreCreate

class GenreService(BaseService):
    def __init__(
        self, 
        genre_repository: GenreRepository, 
        movie_repository: MovieRepository
    ):
        super().__init__(genre_repository)
        self.repository: GenreRepository = genre_repository
        self.repository_movies: MovieRepository = movie_repository

    def get_all(self):
        return self.repository.get_all()
    
    def create(self, data: GenreCreate):
        return self.repository.create(data.model_dump())
    
    def get_by_id_or_fail(self, id: int):
        return self.repository.get_by_id_or_fail(id)
    
    def update(self, id: int, data: GenreCreate):
        genre = self.repository.get_by_id_or_fail(id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(genre, field, value)

        return self.repository.update(genre)
    

    def delete_by_id(self, id: int, confirm: bool = True):
        """
        Elimina un genero, como es una entidad relacionada con peliculas, se realizan algunas operaciones:
            1.- se revisa si existe una pelicula relacionada, en caso de existir las peliculas involucradas se setean al genero
            "sin identificar"
            2.- se elimina el genero
            TODO: en proximas versiones 
            1.- se hara soft delete indicando la fecha de borrado
            2.- se deberá adaptar la consulta de los generos que no se encuentren borrados
            3.- Hay un problema de atomicidad de la operacion, aca hay que implementar UnitOfWork
        Args:
            id (int): id del genero a eliminar
            confirm (bool, optional): para indicar si se desea realizar el borrado, si no, se emula un borrado. Defaults to True.

        Returns:
            _type_: No devuelve nada, no hace falta
        """
        movies = self.repository_movies.get_by_genre_id(id)
        genre_no_identified = self.repository.get_by_id_or_fail(config.GENRE_NOT_IDENTIFIED_ID)
        for movie in movies:
            movie.genre_id = genre_no_identified.id
            self.repository_movies.update(movie)
        
        return self.repository.delete_by_id(id, confirm)

    