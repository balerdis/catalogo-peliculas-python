import logging
from typing import Generic, Optional, TypeVar, Type, Mapping, Any
from sqlalchemy import select


from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")

class EntityNotFoundError(Exception):
    pass

class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: Type[ModelType], session: Session):
        self.model_class = model_class
        self.session = session

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return (
            self.session
            .query(self.model_class)
            .filter(self.model_class.id == id)
            .first()
        )
    
    def get_by_id_or_fail(self, id: int) -> ModelType:
        db_obj = self.get_by_id(id)
        if db_obj is None:
            raise EntityNotFoundError(f"{self.model_class.__name__} con id={id} no encontrado")
        return db_obj

    # este metodo lo pase a Alchemy 2.0, faltan los otros en este repositorio
    def get_all(self
                , offset: int = 0
                , fetch: int = 100
                ) -> list[ModelType]:
        

        smt = select(self.model_class)

        return (
            self.session
            .execute(
                smt
                .offset(offset)
                .limit(fetch)
            )
            .scalars()
            .all()
        )    

        
    def create(self, data: Mapping[str, Any]) -> ModelType:
        try:
            obj = self.model_class(**data)
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            logger.exception(
                "Error creando %s con data=%s",
                self.model_class.__name__,
                data,
            )
            self.session.rollback()
            raise
        
    def update(self, obj: ModelType) -> ModelType:
        try:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            logger.exception(
                "Error al intentar actualizar el %s",
                self.model_class.__name__,
            )
            self.session.rollback()
            raise
        
    def delete(self, db_obj: ModelType) -> None:
        try:
            self.session.delete(db_obj)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            logger.exception(
                "Error eliminando %s",
                self.model_class.__name__,
            )
            raise
        
    def delete_by_id(self, id: int, confirm: bool = True) -> None:
        db_obj = self.get_by_id(id)
        if db_obj is None:
            raise EntityNotFoundError(f"{self.model_class.__name__} con id={id} no encontrado")

        if not confirm:
            return

        self.session.delete(db_obj)
        self.session.commit()
        
    def count(self, **filters) -> int:
        try:
            query = self.session.query(self.model_class)
            for field, value in filters.items():
                if hasattr(self.model_class, field):
                    query = query.filter(getattr(self.model_class, field) == value)

            return query.count()
        except SQLAlchemyError as e:
            logger.exception(
                "Error al intentar contar %s",
                self.model_class.__name__,
            )
            raise
