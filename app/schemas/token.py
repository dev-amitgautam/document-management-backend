from pydantic import BaseModel
from typing import Optional
from app.models.user import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class TokenData(BaseModel):
    user_id: int
    role: UserRole 