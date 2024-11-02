"""
Pet model for interacting with the pets table in the database.
Includes database for medical_info, photos, and events.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Pet(Base):
    """
	Relationships:
		owner (User): The relationship between the pet and its owner, linked to the User model.
	"""
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String)
    age = Column(Integer)
    birth = Column(Date)
    weight = Column(Integer)
    neutered = Column(Boolean, default=False)

    owner = relationship("User", back_populates="pets")

    # medical_info = relationship("MedicalInfo", back_populates="pet", cascade="all, delete-orphan")
    # photos = relationship("Photo", back_populates="pet", cascade="all, delete-orphan")
    # events = relationship("Event", back_populates="pet", cascade="all, delete-orphan")



class MedicalInfo(Base):
    """Medical information for a pet, including medication, allergies, and vet information."""
    __tablename__ = "medical_info"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    medication = Column(String)
    medication_purchase_frequency = Column(Integer)
    vet_card_image_url = Column(String)
    qr_chip_image_url = Column(String)
    allergies = Column(String)  # Puedes almacenar como una lista separada por comas
    illness = Column(String)  # Similar a allergies

    pet = relationship("Pet", back_populates="medical_info")




class Photo(Base):
    """Photos of a pet."""
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    url = Column(String, nullable=False)

    pet = relationship("Pet", back_populates="photos")



class Event(Base):
    """Events for a pet, including vet visits, vaccinations, and birthdays."""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)

    pet = relationship("Pet", back_populates="events")
