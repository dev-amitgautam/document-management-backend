from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_active_user, get_current_admin_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate, UserUpdateRole
from app.services.user import user_service

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update current user.
    """
    return user_service.update_user(db, current_user.id, user_in)

@router.get("", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Retrieve users. Admin only.
    """
    return user_service.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get a specific user by id. Admin only.
    """
    return user_service.get_user(db, user_id)

@router.put("/{user_id}/role", response_model=UserSchema)
def update_user_role(
    user_id: int,
    role_in: UserUpdateRole,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Update a user's role. Admin only.
    """
    return user_service.update_user_role(db, user_id, role_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Delete a user. Admin only.
    """
    user_service.delete_user(db, user_id)
    return None 