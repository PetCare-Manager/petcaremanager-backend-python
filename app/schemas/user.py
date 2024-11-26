"""
Definition of schemas for User
"""
import re
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator

class UserBase(BaseModel):
    """Base schema for a user with the essential attribute email."""
    email: str

class UserLogin(UserBase):
    """Schema for user login, includes email and password."""
    password: str
    @field_validator("email")
    @classmethod
    def must_be_email(cls, value: str):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError("Formato de email inválido")
        return value

    @field_validator("password")
    @classmethod
    def must_be_password(cls, value: str):
        password_regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[!\"#\$%&'\(\)\*\+,\-./:;<=>\?@\[\]\\\^_`{\|}~]).{8,}$"
        if not re.match(password_regex, value):
            raise ValueError("La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, un número y un símbolo especial.")
        return value

class User(UserBase):
    """Schema for returning user information, includes id."""
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserInfo(User):
    """Detailed schema for returning user information, includes username and created_at."""
    username: str
    created_at: datetime

class UserUpdate(BaseModel):
    """Schema for updating user information, currently only allows updating the username."""
    # username: Optional[str]
    name: Optional[str]
    avatar_url: Optional[HttpUrl]
