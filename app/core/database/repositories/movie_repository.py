from .base_repository import BaseRepository
from ..models.models import Movie
from sqlalchemy.orm import Session


import logging
import app.config.config as config


logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

class MovieRepository(BaseRepository[Movie]):
    def __init__(self, session: Session):
        super().__init__(Movie, session)