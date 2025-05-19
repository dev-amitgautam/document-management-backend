from datetime import timedelta
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db.database import get_db
from app.db.repositories.user_repository import user_repository
from app.models.user import User
from app.schemas.token import Token

class AuthService:
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        return user_repository.authenticate(db, username, password)
    
    def create_access_token(self, user: User) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        return Token(access_token=access_token)

auth_service = AuthService() 