from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_active_user, get_current_editor_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.ingestion import Ingestion as IngestionSchema, IngestionCreate, IngestionUpdate
from app.services.ingestion import ingestion_service
from app.services.document import document_service

router = APIRouter()

@router.get("", response_model=List[IngestionSchema])
def read_ingestions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve ingestions.
    """
    return ingestion_service.get_ingestions(db, skip=skip, limit=limit)

@router.post("", response_model=IngestionSchema, status_code=status.HTTP_201_CREATED)
def create_ingestion(
    ingestion_in: IngestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_editor_user),
):
    """
    Trigger a new ingestion process. Editor or admin only.
    """
    # Verify document exists and user has access
    document = document_service.get_document(db, ingestion_in.document_id)
    if document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to ingest this document",
        )
    return ingestion_service.create_ingestion(db, ingestion_in)

@router.get("/{ingestion_id}", response_model=IngestionSchema)
def read_ingestion(
    ingestion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific ingestion by id.
    """
    return ingestion_service.get_ingestion(db, ingestion_id)

@router.put("/{ingestion_id}", response_model=IngestionSchema)
def update_ingestion(
    ingestion_id: int,
    ingestion_in: IngestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_editor_user),
):
    """
    Update an ingestion status. Editor or admin only.
    """
    return ingestion_service.update_ingestion(db, ingestion_id, ingestion_in)

@router.get("/document/{document_id}", response_model=List[IngestionSchema])
def read_document_ingestions(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all ingestions for a specific document.
    """
    # Verify document exists and user has access
    document = document_service.get_document(db, document_id)
    if document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this document's ingestions",
        )
    return ingestion_service.get_document_ingestions(db, document_id) 