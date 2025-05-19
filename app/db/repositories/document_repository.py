from sqlalchemy.orm import Session
from typing import List, Optional
import os
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
import io

from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.core.config import settings

class DocumentRepository:
    def get_by_id(self, db: Session, document_id: int) -> Optional[Document]:
        return db.query(Document).filter(Document.id == document_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Document]:
        return db.query(Document).offset(skip).limit(limit).all()
    
    def get_by_owner(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Document]:
        return db.query(Document).filter(Document.owner_id == owner_id).offset(skip).limit(limit).all()
    
    async def create(self, db: Session, document_in: DocumentCreate, file: UploadFile, owner: User) -> Document:
        try:
            # Reset file cursor position to beginning
            await file.seek(0)
            
            # Read file content
            content = await file.read()
            file_size = len(content)
            
            # Check file size (5MB limit)
            if file_size > 5 * 1024 * 1024:  # 5MB in bytes
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File size exceeds the 5MB limit"
                )
            
            # Create document record with binary data
            db_document = Document(
                title=document_in.title,
                description=document_in.description,
                file_name=file.filename,
                file_type=file.content_type,
                file_size=file_size,
                file_data=content,
                owner_id=owner.id
            )
            
            db.add(db_document)
            db.commit()
            db.refresh(db_document)
            return db_document
            
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            db.rollback()
            # Log the detailed error
            print(f"Error uploading document: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document"
            )
    
    def update(self, db: Session, db_document: Document, document_in: DocumentUpdate) -> Document:
        update_data = document_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_document, field, value)
            
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document
    
    def delete(self, db: Session, document_id: int) -> None:
        db_document = db.query(Document).filter(Document.id == document_id).first()
        if db_document:
            db.delete(db_document)
            db.commit()
    
    def get_file_content(self, db: Session, document_id: int) -> Optional[tuple]:
        """Get file content and metadata for streaming response"""
        document = self.get_by_id(db, document_id)
        if not document:
            return None
        
        return (
            document.file_data, 
            document.file_name, 
            document.file_type
        )

document_repository = DocumentRepository()