from app.api.dependencies.base import get_db_session
from app.core.services.genre_service import GenreService
from app.core.database.repositories.genre_repository import GenreRepository
from app.core.database.repositories.movie_repository import MovieRepository
from sqlalchemy.orm import Session
from fastapi import Depends

def get_genre_service(
        db: Session = Depends(get_db_session)
) -> GenreService:
    return GenreService(
        genre_repository=GenreRepository(db),
        movie_repository=MovieRepository(db)
    )