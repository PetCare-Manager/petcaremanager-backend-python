"""
API Router for Pet Management
Provides endpoints for pet registration, retrieval, update and delete.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from schemas.pet import PetCreate, PetUpdate, PetResponse
from services.pet import PetService

pet_router = APIRouter()

@pet_router.post(
    "/", 
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())]
)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    """
    Creates a new pet.
    Returns:
        PetResponse: The newly created pet data.
    """
    pet_service = PetService(db)
    new_pet = pet_service.create_pet(pet)
    return new_pet

@pet_router.get("/{pet_id}",
    response_model=PetResponse,
    dependencies=[Depends(JWTBearer())]
)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a pet by its unique ID.
    Raises:
        HTTPException: If the pet is not found.
    """
    pet_service = PetService(db)
    pet = pet_service.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@pet_router.patch("/{pet_id}", 
    response_model=PetResponse, 
    dependencies=[Depends(JWTBearer())]
)
def update_pet(pet_id: int, pet_data: PetUpdate, db: Session = Depends(get_db)):
    """
    Updates a pet's information by its unique ID.
    Raises:
        HTTPException: If the pet is not found.
    """
    pet_service = PetService(db)
    updated_pet = pet_service.update_pet(pet_id, pet_data)
    if not updated_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return updated_pet

@pet_router.delete("/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())]
)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    """
    Deletes a pet by its unique ID.
    Raises:
        HTTPException: If the pet is not found.
    """
    pet_service = PetService(db)
    success = pet_service.delete_pet(pet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pet not found")
    return None
