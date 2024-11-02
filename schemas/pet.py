from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class PetBase(BaseModel):
    name: str
    breed: Optional[str] = None
    age: int
    birth: Optional[datetime] = None
    weight: Optional[int] = None
    neutered: bool

    @field_validator("age")
    def age_must_be_positive(self, value: int):
        if value <= 0:
            raise ValueError("Age must be greater than 0")
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
