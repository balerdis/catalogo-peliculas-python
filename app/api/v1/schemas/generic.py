from typing import Annotated, Optional, TypedDict
from pydantic import BaseModel, Field, constr, field_validator
from typing import Generic, TypeVar, List
T = TypeVar("T")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    result: str

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    errors: Optional[list] = None    

class TokenInfo(TypedDict):
    time: float
    usuario_id: int
    usuario_email: str

# Submodelo para "data"
class DataModel(BaseModel):
    description: Annotated[str, constr(min_length=1)] = Field(..., example="texto del caso")

    @field_validator("description")
    def no_only_spaces(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("description no puede estar vacío o contener solo espacios")
        return v

    model_config = {
        "extra": "allow"  
    }  

"""
La idea es tener una response estandar para todos los endpoints de la api
{
  "status": "success",
  "message": "La consulta fue realizada exitosamente",
  "errors": [],
  "data": {
    "id": 3,
    "title": "string",
    "year": 1881
  }
}        
"""
class ApiResponse(BaseModel, Generic[T]):
    status: str
    message: str
    errors: List[str]
    data: T