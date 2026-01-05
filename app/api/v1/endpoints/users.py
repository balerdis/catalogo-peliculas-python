from fastapi import status, APIRouter
from app.core.database.connection import db_connection
from app.api.dependencies.users.providers import get_user_service
from app.api.v1.schemas.users import UserCreate, UserResponse
from app.api.v1.schemas.generic import ApiResponse
from app.core.services.user_service import UserService
from fastapi import Depends

router = APIRouter()
# ###################CREATE USER###################
@router.post("/"
             , response_model=ApiResponse[UserResponse]
             , status_code=status.HTTP_201_CREATED
             , description="Crea una nueva película"
             )
def create_movie(
    request: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.create_user(request)

    return ApiResponse(
        status="success",
        message="El usuario fue creado correctamente",
        errors=[],
        data=UserResponse.model_validate(user)
    )