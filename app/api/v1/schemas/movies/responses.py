from pydantic import BaseModel

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    year: int
    genre: str
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