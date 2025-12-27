from pydantic import BaseModel

from app.api.v1.schemas.genre.responses import GenreResponse

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    year: int
    genre: GenreResponse
    price: float
    duration: int | None
    rating: int | None
    description: str | None

    model_config = {
        "from_attributes": True
    }


class MoviesReportSummary(BaseModel):
    total_movies: int
    total_units: int
    total_price: float


class DeleteMovieResponse(BaseModel):
    id: int