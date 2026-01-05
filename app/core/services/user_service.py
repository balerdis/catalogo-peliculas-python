from app.core.services.base_service import BaseService
from app.core.security import hash_password
from app.core.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork


class UserService(BaseService):

    def create_user(self, data):
        with SqlAlchemyUnitOfWork() as uow:
            data.password = hash_password(data.password)
            user.password = None
            user = uow.users.create(data.model_dump())
        return user