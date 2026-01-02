from pydantic import BaseModel, Field

class MovieListDTO(BaseModel):
    title_order_asc: bool = True
    year_order_asc: bool = False
    price_order_asc: bool = True
    offset: int = 0
    fetch: int = Field(default=100, le=100)