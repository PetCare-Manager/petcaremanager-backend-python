""""
Implementation of the User service to interact with the database.
"""
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User as UserModel
from schemas.user import UserLogin, UserUpdate


class UserService:
    """
    UserService provides methods to interact with the User table in the database.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_id(self, _id: int) -> Optional[UserModel]:
        """Get user by given id."""
        return self.db.query(UserModel).filter(UserModel.id == _id).first()

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get user by given email."""
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def create_user(self, user: UserLogin) -> UserModel:
        """Create a new user in the database"""
        try:
            new_user = UserModel(**vars(user))
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"An error occurred while creating the user: {e}") from e

    def update_user(self, _id: int, user_update: UserUpdate) ->  Optional[UserModel]:
        """Update username by given id."""
        user = self.get_user_by_id(_id)
        if not user:
            return None
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, _id: int) -> bool:
        """Delete user by given id."""
        user = self.get_user_by_id(_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
