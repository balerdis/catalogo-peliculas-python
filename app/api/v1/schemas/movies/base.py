from pydantic import BaseModel, Field, field_validator
from datetime import date

class MovieBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    director: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., gt=1880, lt=2030)
    genre_id: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

    duration: int | None = None
    rating: int | None = None
    description: str | None = None
    is_watched: bool = False

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value > date.today().year + 5:
            raise ValueError("El año no puede ser mayor al actual + 5")
        return value