from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ReviewDecision(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_NEW_DOCUMENT = "REQUEST_NEW_DOCUMENT"
    OVERRIDE_FINDING = "OVERRIDE_FINDING"

class ReviewDecisionRequest(BaseModel):
    decision: str
    reason: str
    override_reason: Optional[str] = None

class ReviewResponse(BaseModel):
    id: str
    review_case_id: str
    document_id: str
    status: str
    decision: Optional[str] = None
    reason: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
