from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.ingestion_repository import ingestion_repository
from app.models.ingestion import Ingestion, IngestionStatus
from app.schemas.ingestion import IngestionCreate, IngestionUpdate
from app.core.exceptions import NotFoundError

class IngestionService:
    def get_ingestion(self, db: Session, ingestion_id: int) -> Ingestion:
        ingestion = ingestion_repository.get_by_id(db, ingestion_id)
        if not ingestion:
            raise NotFoundError(detail=f"Ingestion with id {ingestion_id} not found")
        return ingestion
    
    def get_ingestions(self, db: Session, skip: int = 0, limit: int = 100) -> List[Ingestion]:
        return ingestion_repository.get_all(db, skip, limit)
    
    def get_document_ingestions(self, db: Session, document_id: int) -> List[Ingestion]:
        return ingestion_repository.get_by_document(db, document_id)
    
    def create_ingestion(self, db: Session, ingestion_in: IngestionCreate) -> Ingestion:
        return ingestion_repository.create(db, ingestion_in)
    
    def update_ingestion(self, db: Session, ingestion_id: int, ingestion_in: IngestionUpdate) -> Ingestion:
        ingestion = self.get_ingestion(db, ingestion_id)
        return ingestion_repository.update(db, ingestion, ingestion_in)
    
    def delete_ingestion(self, db: Session, ingestion_id: int) -> None:
        ingestion = self.get_ingestion(db, ingestion_id)
        ingestion_repository.delete(db, ingestion_id)

ingestion_service = IngestionService() 