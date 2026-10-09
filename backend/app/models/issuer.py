import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey
from app.database import Base
import enum

class OrganizationType(str, enum.Enum):
    UNIVERSITY = "UNIVERSITY"
    COLLEGE = "COLLEGE"
    COMPANY = "COMPANY"
    GOVERNMENT = "GOVERNMENT"
    TRAINING_INSTITUTE = "TRAINING_INSTITUTE"
    OTHER = "OTHER"

class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    SUSPENDED = "SUSPENDED"

class Issuer(Base):
    __tablename__ = "issuers"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    organization_name = Column(String, nullable=False)
    organization_type = Column(Enum(OrganizationType), nullable=False)
    official_domain = Column(String, nullable=False)
    official_email = Column(String, nullable=False)
    registration_reference = Column(String)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    verified_at = Column(DateTime, nullable=True)
    verified_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
