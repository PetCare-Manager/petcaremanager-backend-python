"""
Definition of schemas for Pet
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

class PetBase(BaseModel):
    name: str
    breed: Optional[str] = None
    age: int
    birth: Optional[datetime] = None
    weight: Optional[int] = None
    neutered: bool

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, value: int):
        if value <= 0:
            raise ValueError("Edad tiene que ser mayor que 0")
        return value

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[int] = None
    neutered: Optional[bool] = None

class PetResponse(PetBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
