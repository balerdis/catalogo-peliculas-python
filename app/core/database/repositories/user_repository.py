from sqlalchemy.orm import Session, contains_eager
from app.core.database.repositories.base_repository import BaseRepository
from app.core.database.models.users import User

from sqlalchemy import select, or_, func



class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)