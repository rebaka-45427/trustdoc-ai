import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum, ForeignKey, Float, Text, BigInteger
from app.database import Base
import enum

class LifecycleStatus(str, enum.Enum):
    UPLOADED = "UPLOADED"
    ANALYZING = "ANALYZING"
    ANALYZED = "ANALYZED"
    APPROVED = "APPROVED"

class UploadSource(str, enum.Enum):
    ISSUER_UPLOAD = "ISSUER_UPLOAD"
    OWNER_UPLOAD = "OWNER_UPLOAD"

class Document(Base):
    __tablename__ = "documents"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    doc_id = Column(String, unique=True, index=True)
    owner_id = Column(String(36), ForeignKey("users.id"))
    original_filename = Column(String)
    stored_filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(BigInteger)
    sha256_hash = Column(String(64))
    lifecycle_status = Column(Enum(LifecycleStatus), default=LifecycleStatus.UPLOADED)
    ocr_status = Column(String, nullable=True)
    document_type = Column(String, nullable=True)
    document_type_confidence = Column(Float, nullable=True)
    forensic_risk_score = Column(Integer, nullable=True)
    forensic_risk_level = Column(String, nullable=True)
    trust_score = Column(Integer, nullable=True)
    is_demo = Column(Boolean, default=False)
    upload_source = Column(Enum(UploadSource), default=UploadSource.OWNER_UPLOAD)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
