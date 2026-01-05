# app/core/unit_of_work/sqlalchemy_uow.py
from sqlalchemy.orm import Session
from app.core.database.connection import db_connection
from app.core.database.repositories.user_repository import UserRepository
from app.core.unit_of_work.base import UnitOfWork
from app.core.database.repositories import (
    GenreRepository,
    MovieRepository,
    UserRepository,
)

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self):
        self.session: Session | None = None

    def __enter__(self):
        self.session = db_connection.get_db()
        self.genres = GenreRepository(self.session)
        self.movies = MovieRepository(self.session)
        self.users = UserRepository(self.session)
        return self

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def __exit__(self, exc_type, exc, tb):
        super().__exit__(exc_type, exc, tb)
        self.session.close()
