import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Text
from app.database import Base
import enum

class ReviewStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ReviewDecision(str, enum.Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_NEW_DOCUMENT = "REQUEST_NEW_DOCUMENT"
    OVERRIDE_FINDING = "OVERRIDE_FINDING"

class ReviewCase(Base):
    __tablename__ = "review_cases"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    review_case_id = Column(String, unique=True, index=True)
    document_id = Column(String(36), ForeignKey("documents.id"))
    reviewer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.OPEN)
    decision = Column(Enum(ReviewDecision), nullable=True)
    reason = Column(Text, nullable=True)
    override_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
