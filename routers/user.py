"""
API Router for User Management
Provides endpoints for user registration, retrieval, and authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from schemas.user import UserLogin, User, UserUpdate
from models.user import User as UserModel
from services.user import UserService
from utils.jwt_manager import create_token

user_router = APIRouter()

@user_router.post("/users/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    tags=["User"]
)
def create_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Creates a new user with the provided email and password.
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


@user_router.get("/users/{user_id}",
    response_model=User,
    tags=["User"]
)
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


@user_router.patch("/users/",
    response_model=User, tags=["User"],
    dependencies=[Depends(JWTBearer())]
)
def update_user(user_update: UserUpdate, request: Request,  db: Session = Depends(get_db)):
    """
    Updates the user's information, such as username.
    Raises:
        HTTPException: If the user is not found.
    """
    user_service = UserService(db)
    user_email = request.state.email
    user = user_service.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.username:
        user.username = user_update.username #type: ignore
    db.commit()
    db.refresh(user)
    return user

@user_router.delete("/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())],
    tags=["User"]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a user by their unique ID. 
    Raises:
        HTTPException: If the user is not found.
    """
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@user_router.delete("/users/me/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(JWTBearer())],
    tags=["User"]
)
def delete_me(request: Request, db: Session = Depends(get_db)):
    """
    Deletes the authenticated user, we get ID from the token.
    """
    user_service = UserService(db)
    user_email = request.state.email
    user = user_service.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_service.delete_user(int(user.id)) # type: ignore
    db.commit()
    return None

@user_router.post("/login", tags=["Auth"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT token if successful.
    Raises:
        HTTPException: If the credentials are invalid.
    """
    authenticated_user = UserModel.authenticate(db, user.email, user.password)
    if authenticated_user:
        user_email: str = str(authenticated_user.email)
        user_id: int = int(authenticated_user.id)  # type: ignore
        token: str = create_token(user_id, user_email)
        return JSONResponse(status_code=200, content={"token": token})

    raise HTTPException(status_code=400, detail="Invalid credentials")
