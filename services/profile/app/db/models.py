from sqlalchemy import Column, Integer, String
from .db import Base
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# SQLAlchemy model
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)

# Pydantic models
class ProfileCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class ProfileOut(ProfileCreate):
    id: int
    class Config:
        from_attributes = True
