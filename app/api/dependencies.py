from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Generator, Optional

from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise AuthenticationError()
    except JWTError:
        raise AuthenticationError()
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AuthenticationError()
    if not user.is_active:
        raise AuthenticationError(detail="Inactive user")
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise AuthenticationError(detail="Inactive user")
    return current_user

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise AuthorizationError(detail="The user doesn't have enough privileges")
    return current_user

def get_current_editor_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise AuthorizationError(detail="The user doesn't have enough privileges")
    return current_user 