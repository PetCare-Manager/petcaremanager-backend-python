"""
Definition of schemas for Pet
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
from models.pet import Gender


class PetBase(BaseModel):
    name: str
    breed: str
    birth: date
    neutered: bool
    gender: str
    chip_number: Optional[int] = None
    chronic_illnesses: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    neutered: Optional[bool] = None
    gender: Optional[str] = None
    chip_number: Optional[int] = None
    chronic_illnesses: Optional[bool] = False

    @field_validator("chip_number")
    @classmethod
    def chip_must_have_15_numbers(cls, value: Optional[int]):
        if value is not None and len(str(value)) != 15:
            raise ValueError("Tu número de chip debe tener exactamente 15 dígitos")
        return value
    
class DocumentSchema(BaseModel):
    id: int
    url: str
    filename: str

    model_config = ConfigDict(from_attributes=True)
class PetResponse(PetBase):
    id: int
    user_id: int
    avatar: Optional[str] = None
    documents: List[DocumentSchema] = []

    model_config = ConfigDict(from_attributes=True)
