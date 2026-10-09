import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Integer
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String, index=True)
    actor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True, index=True)
    action_details = Column(JSON, nullable=True)
    previous_event_hash = Column(String, nullable=True)
    current_event_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class IdSequence(Base):
    __tablename__ = "id_sequences"
    name = Column(String, primary_key=True)
    current_value = Column(Integer, default=0)
