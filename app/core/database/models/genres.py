# app/core/database/models/genres.py
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

from .mixins import AuditMixin

class Genre(AuditMixin, Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, index=True)

    movies = relationship("Movie", back_populates="genre")

    __table_args__ = (
        Index("ix_genres_active", "habilited", "deleted_at"),
        Index("ix_genres_name", "name"),
    )    