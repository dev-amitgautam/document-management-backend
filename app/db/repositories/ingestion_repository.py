from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.ingestion import Ingestion, IngestionStatus
from app.schemas.ingestion import IngestionCreate, IngestionUpdate

class IngestionRepository:
    def get_by_id(self, db: Session, ingestion_id: int) -> Optional[Ingestion]:
        return db.query(Ingestion).filter(Ingestion.id == ingestion_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Ingestion]:
        return db.query(Ingestion).offset(skip).limit(limit).all()
    
    def get_by_document(self, db: Session, document_id: int) -> List[Ingestion]:
        return db.query(Ingestion).filter(Ingestion.document_id == document_id).all()
    
    def create(self, db: Session, ingestion_in: IngestionCreate) -> Ingestion:
        db_ingestion = Ingestion(
            document_id=ingestion_in.document_id,
            status=IngestionStatus.PENDING
        )
        
        db.add(db_ingestion)
        db.commit()
        db.refresh(db_ingestion)
        return db_ingestion
    
    def update(self, db: Session, db_ingestion: Ingestion, ingestion_in: IngestionUpdate) -> Ingestion:
        update_data = ingestion_in.dict(exclude_unset=True)
        
        # If status is being updated to COMPLETED, set completed_at
        if "status" in update_data and update_data["status"] == IngestionStatus.COMPLETED:
            update_data["completed_at"] = datetime.utcnow()
        
        for field, value in update_data.items():
            setattr(db_ingestion, field, value)
            
        db.add(db_ingestion)
        db.commit()
        db.refresh(db_ingestion)
        return db_ingestion
    
    def delete(self, db: Session, ingestion_id: int) -> None:
        db_ingestion = db.query(Ingestion).filter(Ingestion.id == ingestion_id).first()
        if db_ingestion:
            db.delete(db_ingestion)
            db.commit()

ingestion_repository = IngestionRepository() 