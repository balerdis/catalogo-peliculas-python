from .base import UserBase
from pydantic import Field

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)