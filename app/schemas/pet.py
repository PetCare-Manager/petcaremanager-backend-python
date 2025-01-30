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
    birth: Optional[datetime] = None
    neutered: bool
    gender: str
    chip_number: Optional[int] = None
    chronic_illnesses: Optional[bool] = False

    @field_validator("chip_number")
    @classmethod
    def chip_must_have_15_numbers(cls, value: int):
        if value <= 15:
            raise ValueError("Tu número de chip debe tener 15 dígitos")
        return value

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    neutered: Optional[bool] = None
    gender: Optional[str] = None

class PetResponse(PetBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
