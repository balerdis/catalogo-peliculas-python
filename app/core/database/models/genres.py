from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    Boolean, 
    func, 
    Index
)

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, index=True)

    created_at = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now()
    )

    modificated_at = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    habilited = Column(
        Boolean, 
        nullable=True, 
        server_default="1"
    )

    deleted_at = Column(
        DateTime, 
        nullable=True
    )

    movies = relationship("Movie", back_populates="genre")

    __table_args__ = (
        Index("ix_genres_active", "habilited", "deleted_at"),
        Index("ix_genres_name", "name"),
    )    