from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, LargeBinary

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    file_name = Column(String, nullable=False)  # Original filename
    file_type = Column(String, nullable=False)  # MIME type
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_data = Column(LargeBinary, nullable=False)  # Binary file content
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    ingestions = relationship("Ingestion", back_populates="document", cascade="all, delete-orphan") 