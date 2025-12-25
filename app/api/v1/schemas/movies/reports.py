from pydantic import BaseModel

class MoviesReportSummary(BaseModel):
    total_movies: int
    total_units: int
    total_price: float