"""
User model for interacting with the users table in the database.
"""

import hashlib
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session
from config.database import Base


class User(Base):
    """
    This class defines the structure of the user entity and includes methods for
    authentication and password management.

    Attributes:
        id (int): The unique identifier for each user.
        username (str): The unique username of the user. It may be None.
        email (str): The email address of the user. It must be unique and is required.
        password (str): The hashed password of the user. It is required and stored securely.
        created_at (datetime): The timestamp of when the user was created.
        
    Methods:
        authenticate(cls, db: Session, username: str, password: str) -> Optional["User"]:
            Class method to authenticate a user using their username and password.
            
        create_password(cls, password: str) -> str:
            Class method to hash a password using MD5. It is recommended to use a more secure hashing algorithm.
            
        __repr__(self) -> str:
            Returns a string representation of the User object.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    @classmethod
    def authenticate(cls, db: Session, username: str, password: str) -> Optional["User"]:
        """Authenticate a user by username and password."""
        user = db.query(cls).filter_by(username=username).first()
        if user is None:
            return None
        if user.password == cls.create_password(password): # type: ignore
            return user
        return None

    @classmethod
    def create_password(cls, password: str) -> str:
        """Hash a password using MD5."""
        h = hashlib.md5()
        h.update(password.encode('utf8'))
        return h.hexdigest()

    def __repr__(self):
        return f"<User(username={self.username})>"
