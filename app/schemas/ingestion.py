from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.ingestion import IngestionStatus

class IngestionBase(BaseModel):
    document_id: int

class IngestionCreate(IngestionBase):
    pass

class IngestionUpdate(BaseModel):
    status: Optional[IngestionStatus] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None

class IngestionInDBBase(IngestionBase):
    id: int
    status: IngestionStatus
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Ingestion(IngestionInDBBase):
    pass 