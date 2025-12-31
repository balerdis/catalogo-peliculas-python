from app.api.v1.schemas.users.base import UserBase

class UserResponse(UserBase):
    id: int
    habilited: bool

    model_config = {
        "from_attributes": True
    }