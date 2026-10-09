from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime
from enum import Enum

class LifecycleStatus(str, Enum):
    UPLOADED = "UPLOADED"
    ANALYZING = "ANALYZING"
    ANALYZED = "ANALYZED"
    ISSUER_PENDING = "ISSUER_PENDING"
    ISSUER_VERIFIED = "ISSUER_VERIFIED"
    ISSUER_FAILED = "ISSUER_FAILED"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REGISTERED = "REGISTERED"
    REVOKED = "REVOKED"
    SUPERSEDED = "SUPERSEDED"
    EXPIRED = "EXPIRED"

class DocumentResponse(BaseModel):
    id: str
    doc_id: str
    public_verification_id: Optional[str] = None
    original_filename: str
    file_type: str
    file_size: int
    sha256_hash: str
    lifecycle_status: str
    document_type: Optional[str] = None
    document_type_confidence: Optional[float] = None
    ocr_status: str
    forensic_risk_score: Optional[int] = None
    forensic_risk_level: Optional[str] = None
    trust_score: Optional[int] = None
    is_demo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class DocumentListResponse(BaseModel):
    documents: list
    total: int
    page: int
    page_size: int

class RevokeRequest(BaseModel):
    reason: str
