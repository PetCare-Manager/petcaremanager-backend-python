"""
API Router for User Management
Provides endpoints for user registration, retrieval, and authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.user import UserLogin, User
from models.user import User as UserModel
from services.user import UserService
from utils.jwt_manager import create_token

user_router = APIRouter()

@user_router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["User"])
def create_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Registers a new user with the provided email and password.
    Raises:
        HTTPException: If the email is already registered.
    """
    user_service = UserService(db)
    db_user = user_service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = UserModel.create_password(user.password)
    new_user = user_service.create_user(user)
    return new_user

@user_router.get("/users/{user_id}", response_model=User, tags=["User"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a user by their unique ID.
    Raises:
        HTTPException: If the user is not found.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/login", tags=["Auth"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT token if successful.
    Raises:
        HTTPException: If the credentials are invalid.
    """
    authenticated_user = UserModel.authenticate(db, user.email, user.password)
    if authenticated_user:
        token: str = create_token({"email": user.email})
        return JSONResponse(status_code=200, content={"token": token})

    raise HTTPException(status_code=400, detail="Invalid credentials")
