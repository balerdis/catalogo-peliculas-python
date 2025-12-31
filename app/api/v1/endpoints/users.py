from fastapi import status, APIRouter
from app.core.database.connection import db_connection
from sqlalchemy.orm import Session
from app.core.database.repositories.user_repository import UserRepository
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
    db: Session = Depends(db_connection.get_db),
):
    service = UserService(UserRepository(db))
    user = service.create_user(request)

    return ApiResponse(
        status="success",
        message="El usuario fue creado correctamente",
        errors=[],
        data=UserResponse.model_validate(user)
    )