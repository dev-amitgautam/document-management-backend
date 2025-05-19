from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.auth import auth_service
from app.schemas.token import Token
from app.schemas.user import UserCreate, User
from app.services.user import user_service
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    return user_service.create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_access_token(user)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout the current user.
    
    Note: Since JWT is stateless, this endpoint is primarily for frontend use.
    The frontend should delete the token from storage after calling this endpoint.
    """
    # In a more complex implementation, you could add the token to a blacklist
    # For now, we'll just return a success message
    return {"message": "Successfully logged out"} 