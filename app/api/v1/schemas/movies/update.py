from pydantic import BaseModel

class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None
    genre_id: int | None = None
    price: float | None = None
    duration: int | None = None
    rating: int | None = None
    description: str | None = None
    is_watched: bool | None = None