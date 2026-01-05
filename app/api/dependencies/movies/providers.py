from app.api.dependencies.base import get_db_session
from app.core.services.movie_service import MovieService
from app.core.database.repositories.movie_repository import MovieRepository
from sqlalchemy.orm import Session
from fastapi import Depends

def get_movie_service(
        db: Session = Depends(get_db_session)
) -> MovieService:
    return MovieService(
        repository=MovieRepository(db),
    )