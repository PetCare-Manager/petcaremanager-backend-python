from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    Float as SQLFloat,
    Enum as SQLEnum,
    Text
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from config.database import Base
from models.user import User 

class Gender(PyEnum):
    MALE = "M"
    FEMALE = "F"

"""
¿Por qué lo hemos verificado y corregido así?

"""
class Pet(Base):
    __tablename__ = "pets"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci"  
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth: Mapped[Date] = mapped_column(Date, nullable=False)
    breed: Mapped[str] = mapped_column(String(150), nullable=False)  # Aumentado para razas largas
    weight: Mapped[Optional[float]] = mapped_column(SQLFloat)
    gender: Mapped[Gender] = mapped_column(SQLEnum(Gender, name="gender_enum", validate_strings=True), nullable=False)
    chip_number: Mapped[Optional[str]] = mapped_column(String(50))  # Cambiado a String por si tiene letras
    chronic_illnesses: Mapped[bool] = mapped_column(Boolean, default=False)
    neutered: Mapped[bool] = mapped_column(Boolean, default=False)  # Añadido default
    avatar: Mapped[Optional[str]] = mapped_column(String(255))
    bg_color: Mapped[Optional[str]] = mapped_column(String(7))  # Longitud para código HEX

    owner: Mapped["User"] = relationship("User", back_populates="pets")
    medical_info: Mapped["MedicalInfo"] = relationship(
        "MedicalInfo", 
        back_populates="pet", 
        cascade="all, delete-orphan",
        uselist=False  # Relación one-to-one
    )
    documents: Mapped[List["Document"]] = relationship(
        "Document", 
        back_populates="pet", 
        cascade="all, delete-orphan"
    )
    events: Mapped[List["Event"]] = relationship(
        "Event", 
        back_populates="pet", 
        cascade="all, delete-orphan",
        order_by="Event.date"  # Ordenar eventos por fecha
    )


class MedicalInfo(Base):
    __tablename__ = "medical_info"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4"
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))
    medication: Mapped[Optional[str]] = mapped_column(Text)  # Text para textos largos
    medication_purchase_frequency: Mapped[Optional[int]] = mapped_column(Integer)
    vet_card_image_url: Mapped[Optional[str]] = mapped_column(String(255))
    qr_chip_image_url: Mapped[Optional[str]] = mapped_column(String(255))
    allergies: Mapped[Optional[str]] = mapped_column(Text)  # Text para listas de alergias

    pet: Mapped["Pet"] = relationship("Pet", back_populates="medical_info")


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4"
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[Optional[str]] = mapped_column(String(50))  # Campo adicional recomendado

    pet: Mapped["Pet"] = relationship("Pet", back_populates="documents")


class Event(Base):
    __tablename__ = "events"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4"
    }

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    time: Mapped[Optional[str]] = mapped_column(String(50))  # Campo adicional recomendado
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)  # Campo adicional recomendado

    pet: Mapped["Pet"] = relationship("Pet", back_populates="events")