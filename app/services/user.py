from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.user_repository import user_repository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserUpdateRole
from app.core.exceptions import NotFoundError, BadRequestError

class UserService:
    def get_user(self, db: Session, user_id: int) -> User:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError(detail=f"User with id {user_id} not found")
        return user
    
    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return user_repository.get_all(db, skip, limit)
    
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        # Check if email already exists
        if user_repository.get_by_email(db, user_in.email):
            raise BadRequestError(detail="Email already registered")
        
        # Check if username already exists
        if user_repository.get_by_username(db, user_in.username):
            raise BadRequestError(detail="Username already taken")
        
        return user_repository.create(db, user_in)
    
    def update_user(self, db: Session, user_id: int, user_in: UserUpdate) -> User:
        user = self.get_user(db, user_id)
        
        # Check if email is being updated and already exists
        if user_in.email and user_in.email != user.email:
            if user_repository.get_by_email(db, user_in.email):
                raise BadRequestError(detail="Email already registered")
        
        # Check if username is being updated and already exists
        if user_in.username and user_in.username != user.username:
            if user_repository.get_by_username(db, user_in.username):
                raise BadRequestError(detail="Username already taken")
        
        return user_repository.update(db, user, user_in)
    
    def update_user_role(self, db: Session, user_id: int, role_in: UserUpdateRole) -> User:
        user = self.get_user(db, user_id)
        return user_repository.update_role(db, user, role_in)
    
    def delete_user(self, db: Session, user_id: int) -> None:
        user = self.get_user(db, user_id)
        user_repository.delete(db, user_id)

user_service = UserService() 