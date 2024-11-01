"""
Definition of schemas for User
"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    """Base schema for a user with the essential attribute email."""
    email: str

class UserLogin(UserBase):
    """Schema for user login, includes email and password."""
    password: str

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
    username: str
