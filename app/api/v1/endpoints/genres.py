from fastapi import status, APIRouter, Depends
from app.api.v1.schemas.generic import ApiResponse
from app.api.v1.schemas.genres.responses import GenreResponse, DeleteGenreResponse
from app.api.v1.schemas.genres.create import GenreCreate
from app.core.services.genre_service import GenreService

router = APIRouter()

# ###################CREATE GENRE###################
@router.post("/", 
            response_model=ApiResponse[GenreResponse],
            description="Crea un nuevo genero",
            status_code=status.HTTP_201_CREATED
            )
def create_genre(
    request: GenreCreate, 
):
    service = GenreService()
    genre = service.create(request)

    return ApiResponse(
        status="success",
        message="Genero creado correctamente",
        errors=[],
        data=GenreResponse.model_validate(genre)
    )

# ###################GET ALL GENRES###################
@router.get("/", 
            response_model=ApiResponse[list[GenreResponse]],
            description="Devuelve todos los generos",
            status_code=status.HTTP_200_OK
            )
def get_genres():
    service = GenreService()
    genres = service.get_all()
        
    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[GenreResponse.model_validate(g) for g in genres]
    )

# ###################GET GENRE BY ID###################
@router.get("/{genre_id}", 
            response_model=ApiResponse[GenreResponse],
            description="Devuelve un genero por id",
            status_code=status.HTTP_200_OK
            )
def get_by_id(genre_id: int):
    service = GenreService()
    genre = service.get_by_id_or_fail(genre_id)

    return ApiResponse(
        status="success",
        message="Genero obtenido correctamente",
        errors=[],
        data=GenreResponse.model_validate(genre)
    )

# ####################UPDATE GENRE###################
@router.patch("/{genre_id}", 
            response_model=ApiResponse[GenreResponse],
            description="Actualiza un genero",
            status_code=status.HTTP_200_OK
            )
def update_by_id(
    genre_id: int, 
    request: GenreCreate,
):
    service = GenreService()
    genre_updated = service.update(genre_id, request)

    return ApiResponse(
        status="success",
        message="Genero actualizado correctamente",
        errors=[],
        data=GenreResponse.model_validate(genre_updated)
    )

# ####################DELETE GENRE###################
@router.delete("/{genre_id}", 
            response_model=ApiResponse[DeleteGenreResponse],
            description="Elimina un genero",
            status_code=status.HTTP_200_OK
            )
def delete_by_id(
    genre_id: int, 
):
    service = GenreService()
    service.delete_by_id(genre_id)

    return ApiResponse(
        status="success",
        message="Genero eliminado correctamente",
        errors=[],
        data=DeleteGenreResponse(genre_id=genre_id)
    )
