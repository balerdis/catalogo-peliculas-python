#/app/core/database/models.py
from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime, TIMESTAMP, Boolean, Date, BigInteger, Text, ForeignKey, func, Numeric
from .base import Base
from sqlalchemy.orm import validates

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
    @validates('duration')
    def validate_duration(self, _, value):
        if value < 1 or value > 600:
            raise ValueError("Duration must be between 1 and 600")
    @validates('rating')
    def validate_rating(self, _, value):
        if value < 0 or value > 10:
            raise ValueError("Rating must be between 0 and 10")
    @validates('price')
    def validate_price(self, _, value):
        if value <= 0.0:
            raise ValueError("Price must be greater than 0")
        

