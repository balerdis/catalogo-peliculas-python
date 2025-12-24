from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date

class MovieBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description='Titulo de la pelicula')
    director: str = Field(..., min_length=1, max_length=100, description='Director de la pelicula')
    year: int = Field(..., gt=1880, lt=2030, description='Año de la pelicula')
    genre: str = Field(..., min_length=3, max_length=50, description='Genero principal de la pelicula')
    price: float = Field(..., gt=0.0, description='Precio de la pelicula')

    duration: Optional[int] = Field(
        None, ge=1, le=600, description='Duracion de la pelicula en minutos'
    )

    rating: Optional[int] = Field(
        None, ge=0, le=10, description='Calificacion de la pelicula'
    )

    description: Optional[str] = Field(
        None, max_length=1000, description='Descripcion de la pelicula'
    )


    is_watched: Optional[bool] = Field(
        default=False, description='Indica si la pelicula ha sido vista'
    )

    # VALIDACIONES PERSONALIZADAS
    @field_validator('year')
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value < 1880:
            raise ValueError('El año debe ser mayor o igual a 1880 (inicio del cine moderno)')
        if value > date.today().year + 5:
            raise ValueError('El año debe ser menor o igual a la fecha actual + 5')
        return value
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El título no puede estar vacío o solo con espacios.")
        return value.strip()



class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None
    genre: str | None = None
    price: float | None = None
    duration: int | None = None
    rating: int | None = None
    description: str | None = None
    is_watched: bool | None = None

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    year: int
    genre: str
    price: float
    duration: int
    rating: int
    description: str

    model_config = {
        "from_attributes": True
    }

class MoviesReportSummary(BaseModel):
    """
    Devuelve un dict con:
      - productos_distintos
      - unidades_totales
      - valor_total (float, dos decimales)
    """
    total_movies: int
    total_units: int
    total_price: float

class DeleteMovieResponse(BaseModel):
    id: int    