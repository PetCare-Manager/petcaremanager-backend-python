# Importaciones necesarias para los modelos SQLAlchemy
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

# Enumeración para definir los géneros de las mascotas
class Gender(PyEnum):
    MALE = "M"      # Masculino
    FEMALE = "F"    # Femenino



class Pet(Base):
    """
    Modelo principal que representa una mascota en el sistema.
    Contiene toda la información básica de la mascota y sus relaciones
    con otros modelos como información médica, documentos y eventos.
    """
    __tablename__ = "pets"
    
    # Configuración específica para MySQL con codificación UTF-8
    __table_args__ = {
        "mysql_engine": "InnoDB",           # Motor de almacenamiento InnoDB para transacciones
        "mysql_charset": "utf8mb4",         # Conjunto de caracteres completo UTF-8
        "mysql_collate": "utf8mb4_unicode_ci"  # Collation para comparaciones Unicode
    }

    # Campos de la tabla pets
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ID único auto-incremental
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))  # FK al propietario
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Nombre de la mascota (obligatorio)
    birth: Mapped[Date] = mapped_column(Date, nullable=False)  # Fecha de nacimiento (obligatorio)
    breed: Mapped[str] = mapped_column(String(150), nullable=False)  # Raza (aumentado para razas con nombres largos)
    weight: Mapped[Optional[float]] = mapped_column(SQLFloat)  # Peso (opcional, puede no conocerse)
    gender: Mapped[Gender] = mapped_column(SQLEnum(Gender, name="gender_enum", validate_strings=True), nullable=False)  # Género usando enum
    chip_number: Mapped[Optional[str]] = mapped_column(String(50))  # Número de chip (puede contener letras)
    chronic_illnesses: Mapped[bool] = mapped_column(Boolean, default=False)  # Indica si tiene enfermedades crónicas
    neutered: Mapped[bool] = mapped_column(Boolean, default=False)  # Indica si está esterilizado/castrado
    avatar: Mapped[Optional[str]] = mapped_column(String(255))  # URL de la imagen de avatar
    bg_color: Mapped[Optional[str]] = mapped_column(String(7))  # Color de fondo en formato HEX (#FFFFFF)

    # Relaciones con otras entidades
    owner: Mapped["User"] = relationship("User", back_populates="pets")  # Relación con el propietario
    
    # Relación uno-a-uno con información médica
    medical_info: Mapped["MedicalInfo"] = relationship(
        "MedicalInfo", 
        back_populates="pet", # Relación inversa con MedicalInfo 
        cascade="all, delete-orphan",  # Elimina la info médica si se elimina la mascota
        uselist=False  # Especifica que es una relación uno-a-uno
    )
    
    # Relación uno-a-muchos con documentos
    documents: Mapped[List["Document"]] = relationship(
        "Document", 
        back_populates="pet", 
        cascade="all, delete-orphan"  # Elimina todos los documentos si se elimina la mascota
    )
    
    # Relación uno-a-muchos con eventos, ordenados por fecha
    events: Mapped[List["Event"]] = relationship(
        "Event", 
        back_populates="pet", 
        cascade="all, delete-orphan",  # Elimina todos los eventos si se elimina la mascota
        order_by="Event.date"  # Los eventos se ordenan automáticamente por fecha
    )


class MedicalInfo(Base):
    """
    Modelo que almacena la información médica específica de cada mascota.
    Incluye medicación, frecuencia de compra, imágenes médicas y alergias.
    """
    __tablename__ = "medical_info"
    
    # Configuración para MySQL
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4"
    }

    # Campos de la tabla medical_info
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ID único
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))  # FK a la mascota
    medication: Mapped[Optional[str]] = mapped_column(Text)  # Medicación actual (texto largo)
    medication_purchase_frequency: Mapped[Optional[int]] = mapped_column(Integer)  # Días entre compras de medicación
    vet_card_image_url: Mapped[Optional[str]] = mapped_column(String(255))  # URL de imagen de tarjeta veterinaria
    qr_chip_image_url: Mapped[Optional[str]] = mapped_column(String(255))  # URL de imagen QR del chip
    allergies: Mapped[Optional[str]] = mapped_column(Text)  # Lista de alergias (texto largo)

    # Relación inversa con Pet
    pet: Mapped["Pet"] = relationship("Pet", back_populates="medical_info")


class Document(Base):
    """
    Modelo para almacenar documentos relacionados con cada mascota.
    Puede incluir certificados, informes médicos, fotografías, etc.
    """
    __tablename__ = "documents"
    
    # Configuración para MySQL
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4"
    }

    # Campos de la tabla documents
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ID único
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))  # FK a la mascota
    url: Mapped[str] = mapped_column(String(255), nullable=False)  # URL del documento (obligatorio)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)  # Nombre del archivo (obligatorio)
    file_type: Mapped[Optional[str]] = mapped_column(String(50))  # Tipo de archivo (pdf, jpg, png, etc.)

    # Relación inversa con Pet
    pet: Mapped["Pet"] = relationship("Pet", back_populates="documents")


class Event(Base):
    """
    Modelo para gestionar eventos relacionados con cada mascota.
    Incluye citas veterinarias, vacunaciones, tratamientos, etc.
    """
    __tablename__ = "events"
    
    # Configuración para MySQL
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4"
    }

    # Campos de la tabla events
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # ID único
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))  # FK a la mascota
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Nombre del evento (obligatorio)
    date: Mapped[Date] = mapped_column(Date, nullable=False)  # Fecha del evento (obligatorio)
    time: Mapped[Optional[str]] = mapped_column(String(50))  # Hora del evento (formato texto por flexibilidad)
    description: Mapped[Optional[str]] = mapped_column(Text)  # Descripción detallada del evento
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)  # Indica si el evento ya se completó

    # Relación inversa con Pet
    pet: Mapped["Pet"] = relationship("Pet", back_populates="events")