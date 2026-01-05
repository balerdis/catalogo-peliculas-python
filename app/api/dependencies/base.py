from sqlalchemy.orm import Session
from app.core.database.connection import db_connection
from typing import Generator

def get_db_session() -> Generator[Session, None, None]:
    for db in db_connection.get_db():
        yield db