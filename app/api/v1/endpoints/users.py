from fastapi import status, APIRouter
from app.api.v1.schemas.users import UserCreate, UserResponse
from app.api.v1.schemas.generic import ApiResponse
from app.core.services.user_service import UserService


router = APIRouter()
# ###################CREATE USER###################
@router.post("/"
             , response_model=ApiResponse[UserResponse]
             , status_code=status.HTTP_201_CREATED
             , description="Crea un nuevo usuario"
             )
def create_movie(
    request: UserCreate,
):
    service = UserService()
    user = service.create_user(request)

    return ApiResponse(
        status="success",
        message="El usuario fue creado correctamente",
        errors=[],
        data=user
    )