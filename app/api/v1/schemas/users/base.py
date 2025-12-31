from pydantic import BaseModel, Field, field_validator, EmailStr


"""class User(Base):
__tablename__ = "users"
id = Column(Integer, primary_key=True)
name = Column(String(255), index=False)
last_name = Column(String(255), index=False)
address = Column(String(255), index=False)
email = Column(String(255), unique=True, index=True, nullable=False)
password = Column(String(255), index=False)
created_at = Column(DateTime,     nullable=False,     server_default=func.now())
modificated_at = Column(    DateTime,     nullable=False,     server_default=func.now(),     onupdate=func.now())
habilited = Column(    Boolean,     nullable=True,     server_default="1")
deleted_at = Column(    DateTime,     nullable=True)
"""
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    last_name: str = Field(..., min_length=3, max_length=100)
    address: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        return v.lower()