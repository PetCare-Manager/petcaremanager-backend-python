"""
Definition of schemas for Pet
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from models.pet import Gender 



class PetBase(BaseModel):
    name: str
    breed: str
    birth: date
    gender: Gender
    breed: str
    chip: Optional[str]
    illness: bool
    neutered: bool
    weight: Optional[float] = None

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    weight: Optional[float] = None
    neutered: Optional[bool] = None

class PetResponse(PetBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
