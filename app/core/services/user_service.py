from app.core.services.base_service import BaseService
from app.core.database.repositories.user_repository import UserRepository
from app.core.security import hash_password

class UserService(BaseService):

    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.repository: UserRepository = repository

    def create_user(self, data):
        data.password = hash_password(data.password)

        user = self.repository.create(data.model_dump())
        user.password = None
        return user