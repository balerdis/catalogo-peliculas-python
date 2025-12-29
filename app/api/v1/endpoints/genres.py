from fastapi import status, APIRouter, Depends
from app.core.database.connection import db_connection
from sqlalchemy.orm import Session
from app.core.database.repositories.base_repository import BaseRepository
from app.core.database.models.models import Genre
from app.api.v1.schemas.generic import ApiResponse
from app.api.v1.schemas.genres.responses import GenreResponse


router = APIRouter()


@router.get("/", 
            response_model=ApiResponse[list[GenreResponse]],
            description="Devuelve todos los generos",
            status_code=status.HTTP_200_OK
            )
async def get_genres(db: Session = Depends(db_connection.get_db)):
    repo = BaseRepository(Genre, db)
    genres = repo.get_all()
        
    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[GenreResponse.model_validate(g) for g in genres]
    )
