"""
Implementation of the Pet service to interact with the database.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models.pet import Pet as PetModel
from schemas.pet import PetCreate, PetUpdate


class PetService:
    """
    PetService provides methods to interact with the Pet table in the database.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_pet_by_id(self, pet_id: int) -> Optional[PetModel]:
        """Get pet by given ID."""
        return self.db.query(PetModel).filter(PetModel.id == pet_id).first()
    def get_pets(self, user_id: int) -> List[PetModel]:
        """Fetch all pets belonging to the given user_id."""
        return self.db.query(PetModel).filter(PetModel.user_id == user_id).all()

    def create_pet(self, pet_data: PetCreate, user_id: int) -> PetModel:
        """Create a new pet in the database."""
        try:
            pet_data_dict = vars(pet_data)
            pet_data_dict["user_id"] = user_id

            new_pet = PetModel(**vars(pet_data))
            self.db.add(new_pet)
            self.db.commit()
            self.db.refresh(new_pet)
            return new_pet
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"An error occurred while creating the pet: {e}") from e

    def update_pet(self, pet_id: int, pet_data: PetUpdate) -> Optional[PetModel]:
        """Update pet information by given ID."""
        pet = self.get_pet_by_id(pet_id)
        if not pet:
            return None
        for key, value in pet_data.model_dump(exclude_unset=True).items():
            setattr(pet, key, value)
        self.db.commit()
        self.db.refresh(pet)
        return pet

    def delete_pet(self, pet_id: int) -> bool:
        """Delete pet by given ID."""
        pet = self.get_pet_by_id(pet_id)
        if not pet:
            return False
        self.db.delete(pet)
        self.db.commit()
        return True
