from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class PublicVerificationEvent(Base):
    __tablename__ = "public_verification_events"
    
    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=True, index=True)
    verification_id_queried = Column(String, nullable=False)
    verifier_ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    result = Column(String, nullable=False)  # FOUND, NOT_FOUND, REVOKED
    created_at = Column(DateTime, default=datetime.utcnow)
