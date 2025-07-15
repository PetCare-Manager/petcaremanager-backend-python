"""
Pet model for interacting with the pets table in the database.
Includes database for medical_info, photos, and events.
"""
from enum import Enum as PyEnum
from typing import List, Optional
from sqlalchemy import Integer, String, Boolean, Date, ForeignKey, Float as SQLFloat, Enum as SQLEnum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from config.database import Base
from models.user import User

class Gender(PyEnum):
    MALE = "M"
    FEMALE = "F"

from sqlalchemy import Enum

class Pet(Base):
    """
	Relationships:
		owner (User): The relationship between the pet and its owner, linked to the User model.
	"""
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    birth: Mapped[Date] = mapped_column(Date, nullable=False)
    breed: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[float] = mapped_column(SQLFloat, nullable=True)
    gender: Mapped[str] = mapped_column(SQLEnum(Gender, name="gender_enum", validate_strings=True), nullable=False)
    chip_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    chronic_illnesses: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    neutered: Mapped[bool] = mapped_column(Boolean, nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="pets")
    medical_info: Mapped["MedicalInfo"] = relationship("MedicalInfo", back_populates="pet", cascade="all, delete-orphan", order_by="Document.id")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="pet", cascade="all, delete-orphan")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="pet", cascade="all, delete-orphan")
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    bg_color: Mapped[str] = mapped_column(String, nullable=True)


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

    pet: Mapped["Pet"] = relationship("Pet", back_populates="medical_info")

class Document(Base):
    """Documents of a pet."""
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    pet: Mapped["Pet"] = relationship("Pet", back_populates="documents")

class Event(Base):
    """Events for a pet."""
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)

    pet: Mapped["Pet"] = relationship("Pet", back_populates="events")
