"""
API Router for Pet Management
Provides endpoints for pet registration, retrieval, update and delete.
"""
from typing import List
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from schemas.pet import PetCreate, PetUpdate, PetResponse, DocumentSchema
from services.pet import PetService
from models.pet import Pet as PetModel, Document
#from models.pet import Document
from utils.upload_service import upload_to_cloudinary

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
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "La mascota no fue encontrada"}
        )
    
    if pet.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "No tienes permiso para modificar esta mascota"}
        )
    updated_pet = pet_service.update_pet(pet_id, pet_data)

    return updated_pet

@pet_router.delete("/{pet_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())]
)
def delete_pet(pet_id: int, request: Request, db: Session = Depends(get_db)) -> bool:
    """
    Deletes a pet by its unique ID, but only if it belongs to the authenticated user.
    Raises:
        HTTPException: If the pet is not found or does not belong to the user.
    """
    user_id = request.state.user_id
    pet_service = PetService(db)
    pet = pet_service.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "La mascota no fue encontrada"}
        )
    
    if pet.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "No tienes permiso para eliminar esta mascota"}
        )

    was_deleted = pet_service.delete_pet(pet_id)

    return was_deleted

@pet_router.post(
    "/{pet_id}/avatar", 
    response_model=PetResponse, 
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())]
)
async def upload_pet_avatar(
    pet_id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1) Verifica que la mascota existe y pertenece al usuario
    pet = db.get(PetModel, pet_id)
    if not pet or pet.user_id != request.state.user_id:
        raise HTTPException(status_code=404, detail="Mascota no encontrada o no pertenece al usuario")
    
    # 2) Sube la imagen y extrae solo la URL
    url = await upload_to_cloudinary(file, folder=f"petcare/pets/{pet_id}/avatar")
    # 3) Guarda la URL en la BD
    pet.avatar = url
    db.commit()
    db.refresh(pet)
    return pet
    #return {"id": pet.id, "avatar": pet.avatar}

@pet_router.post(
    "/{pet_id}/documents",
    response_model=List[DocumentSchema],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())]
)
async def upload_pet_documents(
    pet_id: int,
    request: Request,
    files: List[UploadFile] = File(..., max_items=5),
    db: Session = Depends(get_db)
):
    # 1) Verifica que la mascota existe y pertenece al usuario
    pet = db.get(PetModel, pet_id)
    if not pet or pet.user_id != request.state.user_id:
        raise HTTPException(status_code=404, detail="Mascota no encontrada o no pertenece al usuario")
    
    # 2) Controla que no supere el límite de 5 documentos
    existing = len(pet.documents)
    if existing + len(files) > 5:
        raise HTTPException(
             status_code=400,
             detail=f"Already {existing} documents, you can upload up to 5 total"
         )
    created: List[Document] = []
    for file in files:
        url, filename = await upload_to_cloudinary(
            file, folder=f"petcare/pets/{pet_id}/documents"
        )
        doc = Document(pet_id=pet_id, url=url, filename=filename)
        db.add(doc)
        created.append(doc)
    db.commit()
    for doc in created:
        db.refresh(doc)
    return created