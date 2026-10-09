from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class RegistrationRecord(Base):
    __tablename__ = "registration_records"
    
    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("documents.id"), unique=True, nullable=False)
    registered_by = Column(String, ForeignKey("users.id"), nullable=False)
    public_verification_id = Column(String, unique=True, nullable=False, index=True)
    hmac_token = Column(String, nullable=False)
    qr_code_path = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
