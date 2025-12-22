import logging
from typing import Generic, Optional, TypeVar, Dict, Any, Generic

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: type, session: Session):
        self.model_class = model_class
        self.session = session

    def get_by_id(self, id: int) -> Optional[ModelType]:
        try:
            return self.session.query(self.model_class).filter(self.model_class.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar trabajar con {self.model_class.__name__} por el id {id}: {e}")

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        try:
            return self.session.query(self.model_class).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar trabajar con {self.model_class.__name__}: {e}")
            return []
        
    def create(self, obj_data: Dict[str, Any]) -> Optional[ModelType]:
        db_obj = self.model_class(**obj_data)
        try:
            self.session.add(db_obj)
            self.session.flush()
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar crear {self.model_class.__name__}: {e}")
            self.session.rollback()
            return None
        
    def update(self, db_obj: ModelType, update_data: Dict[str, Any]) -> Optional[ModelType]:
        try:
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            self.session.flush()
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar actualizar {self.model_class.__name__}: {e}")
            self.session.rollback()
            return None
        
    def delete(self, db_obj: ModelType) -> bool:
        try:
            self.session.delete(db_obj)
            self.session.flush()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar eliminar {self.model_class.__name__}: {e}")
            self.session.rollback()
            return False
        
    def delete_by_id(self, id: int) -> bool:
        try:
            db_obj = self.get_by_id(id)
            if db_obj:
                return self.delete(db_obj)
            return False
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar eliminar {self.model_class.__name__} por el id {id}: {e}")
            return False
        
    def exists(self, **filters) -> bool:
        try:
            query = self.session.query(self.model_class)
            for field, value in filters.items():
                if hasattr(self.model_class, field):
                    query = query.filter(getattr(self.model_class, field) == value)

            return query.first() is not None
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar verificar la existencia de {self.model_class.__name__}: {e}")
            return False
        
    def count(self, **filters) -> int:
        try:
            query = self.session.query(self.model_class)
            for field, value in filters.items():
                if hasattr(self.model_class, field):
                    query = query.filter(getattr(self.model_class, field) == value)

            return query.count()
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar contar {self.model_class.__name__}: {e}")
            return 0
