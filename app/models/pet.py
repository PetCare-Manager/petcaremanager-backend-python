"""
Pet model for interacting with the pets table in the database.
Includes database for medical_info, photos, and events.
"""
from typing import List, Optional
from sqlalchemy import Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from config.database import Base
from models.user import User

class Pet(Base):
    """
	Relationships:
		owner (User): The relationship between the pet and its owner, linked to the User model.
	"""
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    breed: Mapped[Optional[str]] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    birth: Mapped[Optional[Date]] = mapped_column(Date)
    weight: Mapped[Optional[int]] = mapped_column(Integer)
    neutered: Mapped[bool] = mapped_column(Boolean, default=False)

    owner: Mapped["User"] = relationship("User", back_populates="pets")
    medical_info: Mapped["MedicalInfo"] = relationship("MedicalInfo", back_populates="pet", cascade="all, delete-orphan")
    photos: Mapped[List["Photo"]] = relationship("Photo", back_populates="pet", cascade="all, delete-orphan")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="pet", cascade="all, delete-orphan")


class MedicalInfo(Base):
    """Medical information for a pet, including medication, allergies, and vet information."""
    __tablename__ = "medical_info"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)
    medication: Mapped[Optional[str]] = mapped_column(String)
    medication_purchase_frequency: Mapped[Optional[int]] = mapped_column(Integer)
    vet_card_image_url: Mapped[Optional[str]] = mapped_column(String)
    qr_chip_image_url: Mapped[Optional[str]] = mapped_column(String)
    allergies: Mapped[Optional[str]] = mapped_column(String)
    illness: Mapped[Optional[str]] = mapped_column(String)

    pet: Mapped["Pet"] = relationship("Pet", back_populates="medical_info")




class Photo(Base):
    """Photos of a pet."""
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    pet: Mapped["Pet"] = relationship("Pet", back_populates="photos")



class Event(Base):
    """Events for a pet."""
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)

    pet: Mapped["Pet"] = relationship("Pet", back_populates="events")
