import logging
from typing import Generic, Optional, TypeVar, Type, Mapping, Any
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions.domain.duplicate_entry import DuplicateEntityError

from datetime import datetime

import pytz
tz = pytz.timezone("America/Argentina/Buenos_Aires")


logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")

class EntityNotFoundError(Exception):
    pass

class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: Type[ModelType], session: Session):
        self.model_class = model_class
        self.session = session

    # se filtran los borrados via soft delete
    def get_by_id(self, id: int) -> Optional[ModelType]:
        smt = (
            select(self.model_class)
              .where(
                  self.model_class.id == id,
                  self.model_class.habilited.is_(True),
                  self.model_class.deleted_at.is_(None)
               )
        )
        result = self.session.execute(smt).scalar_one_or_none()
        return result
    
    def get_by_id_or_fail(self, id: int) -> ModelType:
        db_obj = self.get_by_id(id)
        if db_obj is None:
            raise EntityNotFoundError(f"{self.model_class.__name__} con id={id} no encontrado")
        return db_obj

    # se filtran los borrados via soft delete
    def get_all(self
                , offset: int = 0
                , fetch: int = 100
                ) -> list[ModelType]:
        

        smt = (
            select(self.model_class)
            .where(
                self.model_class.habilited.is_(True),
                self.model_class.deleted_at.is_(None)
                )
            .offset(offset)
            .limit(fetch)
        )

        return (
            self.session
            .execute(smt)
            .scalars()
            .all()
        )    


    def create(self, data: dict, unique_field: Optional[str] = "name") -> ModelType:
        try:
            entity = self.model_class(**data)
            self.session.add(entity)
            self.session.flush()
            return entity

        except IntegrityError as e:
            self.session.rollback()

            # MySQL duplicate key
            if "Duplicate entry" in str(e.orig):
                raise DuplicateEntityError(
                    entity=self.model_class.__name__,
                    field=unique_field,
                    value=data.get(unique_field)
                ) from e

            raise

    def update(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        return obj

    # Se hacen soft delete siempre
    def delete(self, db_obj: ModelType) -> None:
        db_obj.habilited = False
        db_obj.deleted_at = datetime.now(tz)
        self.session.add(db_obj)

    def delete_by_id(self, id: int, confirm: bool = True) -> None:
        if not confirm:
            return
        obj = self.get_by_id_or_fail(id)
        self.delete(obj)
        
    def count(self, **filters) -> int:
        try:
            stmt = (
                select(func.count())
                    .select_from(self.model_class)
                    .where(
                        self.model_class.habilited.is_(True),
                        self.model_class.deleted_at.is_(None)
                    )
                )

            for field, value in filters.items():
                if hasattr(self.model_class, field):
                    stmt = stmt.where(
                        getattr(self.model_class, field) == value
                    )


            return self.session.execute(stmt).scalar_one()

        except SQLAlchemyError:
            logger.exception(
                "Error contando %s",
                self.model_class.__name__,
            )
            raise
