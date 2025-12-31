import email
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Boolean, 
    DateTime, 
    func,
)

from .base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=False)
    last_name = Column(String(255), index=False)
    address = Column(String(255), index=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), index=False)

    created_at = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now()
    )

    modificated_at = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    habilited = Column(
        Boolean, 
        nullable=True, 
        server_default="1"
    )

    deleted_at = Column(
        DateTime, 
        nullable=True
    )