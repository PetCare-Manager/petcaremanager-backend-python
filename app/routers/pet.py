"""
API Router for Pet Management
Provides endpoints for pet registration, retrieval, update and delete.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
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
def create_pet(pet: PetCreate, request: Request, db: Session = Depends(get_db)):
    """
    Creates a new pet for the authenticated user.
    Returns:
        PetResponse: The newly created pet data.
    """
    user_id = request.state.user_id
    pet_service = PetService(db)
    new_pet = pet_service.create_pet(pet, user_id)
    return new_pet

# @pet_router.get("/{pet_id}",
#     response_model=PetResponse,
#     dependencies=[Depends(JWTBearer())]
# )
# def get_pet(pet_id: int, db: Session = Depends(get_db)):
#     """
#     Retrieves a pet by its unique ID.
#     Raises:
#         HTTPException: If the pet is not found.
#     """
#     pet_service = PetService(db)
#     pet = pet_service.get_pet_by_id(pet_id)
#     if not pet:
#         raise HTTPException(status_code=404, detail="Pet not found")
#     return pet

@pet_router.get("/", response_model=List[PetResponse], dependencies=[Depends(JWTBearer())])
def get_pets(request: Request, db: Session = Depends(get_db)):
    """
    Retrieves all pets belonging to the authenticated user.
    Returns:
        List[PetResponse]: A list of pets owned by the authenticated user.
    """
    user_id = request.state.user_id
    pet_service = PetService(db)
    pets = pet_service.get_pets(user_id)
    return pets

@pet_router.patch("/{pet_id}",
    response_model=PetResponse,
    dependencies=[Depends(JWTBearer())]
)
def update_pet(pet_id: int, pet_data: PetUpdate, request: Request, db: Session = Depends(get_db)):
    """
    Updates a pet's information by its unique ID.
    Raises:
        HTTPException: If the pet is not found.
    """
    user_id = request.state.user_id
    pet_service = PetService(db)
    pet = pet_service.get_pet_by_id(pet_id)
    if not pet or pet.user_id != user_id:
        raise HTTPException(status_code=404, detail="Pet not found or does not belong to the user")
    updated_pet = pet_service.update_pet(pet_id, pet_data)
    if not updated_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return updated_pet

@pet_router.delete("/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())]
)
def delete_pet(pet_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Deletes a pet by its unique ID, but only if it belongs to the authenticated user.
    Raises:
        HTTPException: If the pet is not found or does not belong to the user.
    """
    user_id = request.state.user_id
    pet_service = PetService(db)
    pet = pet_service.get_pet_by_id(pet_id)
    if not pet or pet.user_id != user_id:
        raise HTTPException(status_code=404, detail="Pet not found or does not belong to the user")
    success = pet_service.delete_pet(pet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pet not found")
    return None
