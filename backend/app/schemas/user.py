from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ISSUER = "ISSUER"
    DOCUMENT_OWNER = "DOCUMENT_OWNER"
    REVIEWER = "REVIEWER"

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdateRequest(BaseModel):
    role: Optional[str] = None
    is_active: Optional[bool] = None
    full_name: Optional[str] = None

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str  # Admin only endpoint - can set any role
