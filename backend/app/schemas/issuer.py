from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class OrgType(str, Enum):
    UNIVERSITY = "UNIVERSITY"
    COLLEGE = "COLLEGE"
    COMPANY = "COMPANY"
    GOVERNMENT = "GOVERNMENT"
    TRAINING_INSTITUTE = "TRAINING_INSTITUTE"
    OTHER = "OTHER"

class IssuerCreateRequest(BaseModel):
    organization_name: str
    organization_type: str
    official_domain: str
    official_email: EmailStr
    registration_reference: Optional[str] = None
    is_demo: bool = False

class IssuerResponse(BaseModel):
    id: str
    organization_name: str
    organization_type: str
    official_domain: str
    official_email: str
    registration_reference: Optional[str] = None
    verification_status: str
    verified_at: Optional[datetime] = None
    is_demo: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class IssuerVerifyRequest(BaseModel):
    notes: Optional[str] = None
