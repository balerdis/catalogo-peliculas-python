from app.api.dependencies.base import get_db_session
from app.core.services.user_service import UserService
from app.core.database.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from fastapi import Depends

def get_user_service(
        db: Session = Depends(get_db_session)
) -> UserService:
    return UserService(
        repository=UserRepository(db),
    )