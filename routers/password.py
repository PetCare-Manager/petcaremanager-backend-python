"""
Routes and logic for password reset functionality in the PetCare Manager application.
    - POST /api/auth/password/: Initiates a password reset for a given email.
    - POST /api/auth/password/confirm: Resets the user's password using a valid reset token.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.user import User as UserModel
from schemas.password import PasswordResetConfirm, PasswordResetRequest
from services.user import UserService
from utils.email_service import send_password_reset_email
from utils.jwt_manager import create_reset_token, validate_reset_token

pass_router = APIRouter()

@pass_router.post("/", tags=["Auth"])
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Initiates a password reset for the given email.
    Sends an email with a reset link if the email is registered.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = create_reset_token(request.email)
    send_password_reset_email(request.email, reset_token)

    return {"message": "Password reset email sent", "token": reset_token}

@pass_router.post("/confirm", tags=["Auth"])
def reset_password_confirm(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Resets the user's password using a valid reset token.
    """
    email = validate_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = UserModel.create_password(request.new_password)
    user.password = hashed_password #type: ignore
    db.commit()
    return {"message": "Password has been reset successfully"}
