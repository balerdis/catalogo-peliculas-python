#/app/core/database/models.py
from sqlalchemy import (
    CheckConstraint, 
    Column, 
    Integer, 
    String, 
    DateTime, 
    TIMESTAMP, 
    Boolean, 
    Date, 
    BigInteger, 
    Text, 
    ForeignKey, 
    func, 
    Numeric,
    Index
)
from sqlalchemy.orm import validates, relationship
from .base import Base


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, index=True)

    falta = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now()
    )

    fmodificacion = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    habilitado = Column(
        Boolean, 
        nullable=True, 
        server_default="1"
    )

    feliminado = Column(
        DateTime, 
        nullable=True
    )

    movies = relationship("Movie", back_populates="genre")

    __table_args__ = (
        Index("ix_genres_active", "habilitado", "feliminado"),
        Index("ix_genres_name", "name"),
    )    

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    director = Column(String(100), nullable=False)

    year = Column(Integer, index=True, nullable=False)

    genre = Column(String(50), index=True, nullable=False)

    duration = Column(Integer, nullable=True)
    rating = Column(Integer, index=True)

    description = Column(String(1000), nullable=True)

    price = Column(Numeric(10, 2), index=True, nullable=False)

    is_watched = Column(Boolean, index=True, nullable=False, default=False)

    genre_id = Column(
        Integer, 
        ForeignKey("genres.id", ondelete="NO ACTION", onupdate="NO ACTION"), 
        nullable=False,
        index=True
    )

    genre = relationship("Genre", back_populates="movies", lazy="joined")

    __table_args__ = (
        CheckConstraint('year >= 1880 and year <= 2030', name='year_constraint'),
        CheckConstraint('duration >= 1 AND duration <= 600', name='duration_constraint'),
        CheckConstraint('rating >= 0 and rating <= 10', name='rating_constraint'),
        CheckConstraint('price > 0', name='price_constraint'),
        
    )

    @validates('year')
    def validate_year(self, _, value):
        if value < 1880 or value > 2030:
            raise ValueError("Year must be between 1880 and 2030")
        return value
    @validates('duration')
    def validate_duration(self, _, value):
        if value is None:
            return value
        if value < 1 or value > 600:
            raise ValueError("Duration must be between 1 and 600")
        return value
    @validates('rating')
    def validate_rating(self, _, value):
        if value is None:
            return value        
        if value < 0 or value > 10:
            raise ValueError("Rating must be between 0 and 10")
        return value
    @validates('price')
    def validate_price(self, _, value):
        if value is None:
            return value        
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value
        

