from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from ..models.models import Movie


class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session: Session):
        super().__init__(Movie, session)