from fastapi import APIRouter, Depends, File, UploadFile, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import io

from app.api.dependencies import get_current_active_user, get_current_editor_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import Document as DocumentSchema, DocumentCreate, DocumentUpdate
from app.services.document import document_service
from app.db.repositories.document_repository import document_repository

router = APIRouter()

@router.get("", response_model=List[DocumentSchema])
def read_documents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve documents.
    """
    if current_user.role == "admin":
        return document_service.get_documents(db, skip=skip, limit=limit)
    return document_service.get_user_documents(db, current_user.id, skip=skip, limit=limit)

@router.post("", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
async def create_document(
    document_in: DocumentCreate = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_editor_user),
):
    """
    Create new document. Editor or admin only.
    """
    return await document_service.create_document(db, document_in, file, current_user)

@router.get("/{document_id}", response_model=DocumentSchema)
def read_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific document by id.
    """
    document = document_service.get_document(db, document_id)
    # Check if user is owner or admin
    if document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this document",
        )
    return document

@router.put("/{document_id}", response_model=DocumentSchema)
def update_document(
    document_id: int,
    document_in: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_editor_user),
):
    """
    Update a document. Editor or admin only.
    """
    return document_service.update_document(db, document_id, document_in, current_user)

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_editor_user),
):
    """
    Delete a document. Editor or admin only.
    """
    document_service.delete_document(db, document_id, current_user)

@router.get("/{document_id}/download")
def download_document(
    document_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Download a document file.
    """
    # Check document exists and user has permission
    document = document_service.get_document(db, document_id)
    if document.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to download this document",
        )
    
    # Get file content and metadata
    file_data = document_repository.get_file_content(db, document_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="Document not found")
    
    content, filename, content_type = file_data
    
    # Return streaming response
    return StreamingResponse(
        io.BytesIO(content),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    ) 