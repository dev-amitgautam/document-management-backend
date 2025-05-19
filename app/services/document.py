from typing import List
from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.document_repository import document_repository
from app.models.document import Document
from app.models.user import User, UserRole
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.core.exceptions import NotFoundError, AuthorizationError

class DocumentService:
    def get_document(self, db: Session, document_id: int) -> Document:
        document = document_repository.get_by_id(db, document_id)
        if not document:
            raise NotFoundError(detail=f"Document with id {document_id} not found")
        return document
    
    def get_documents(self, db: Session, skip: int = 0, limit: int = 100) -> List[Document]:
        return document_repository.get_all(db, skip, limit)
    
    def get_user_documents(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Document]:
        return document_repository.get_by_owner(db, user_id, skip, limit)
    
    async def create_document(self, db: Session, document_in: DocumentCreate, file: UploadFile, current_user: User) -> Document:
        return await document_repository.create(db, document_in, file, current_user)
    
    def update_document(self, db: Session, document_id: int, document_in: DocumentUpdate, current_user: User) -> Document:
        document = self.get_document(db, document_id)
        
        # Check if user is owner or admin
        if document.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise AuthorizationError(detail="Not enough permissions to update this document")
        
        return document_repository.update(db, document, document_in)
    
    def delete_document(self, db: Session, document_id: int, current_user: User) -> None:
        document = self.get_document(db, document_id)
        
        # Check if user is owner or admin
        if document.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise AuthorizationError(detail="Not enough permissions to delete this document")
        
        document_repository.delete(db, document_id)

document_service = DocumentService() 