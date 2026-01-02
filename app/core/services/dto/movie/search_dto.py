from pydantic import BaseModel, Field
from typing import Optional

class MovieSearchDTO(BaseModel):
    search: Optional[str] = None
    year_order_asc: bool = False
    price_order_asc: bool = False
    price_min: float = 0.0
    price_max: Optional[float] = None
    offset: int = 0
    fetch: int = Field(default=100, le=100)