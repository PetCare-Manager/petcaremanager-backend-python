"""
User model for interacting with the user table in the database.
"""

from typing import Optional
from datetime import datetime
import bcrypt
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session, relationship
from config.database import Base


class User(Base):
    """
    This class defines the structure of the user entity and includes methods for
    authentication and password management.

    Methods:
        authenticate(cls, db: Session, username: str, password: str) -> Optional["User"]:
            Class method to authenticate a user using their username and password.
            
        create_password(cls, password: str) -> str:
            Class method to hash a password.
            
        __repr__(self) -> str:
            Returns a string representation of the User object.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    pets = relationship("Pet", back_populates="owner")

    @classmethod
    def authenticate(cls, db: Session, email: str, password: str) -> Optional["User"]:
        """Authenticate a user by email and password."""
        user = db.query(cls).filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        return None

    @classmethod
    def create_password(cls, password: str) -> str:
        """Hash a password using bcrypt."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def __repr__(self):
        return f"<User(username={self.username})>"
