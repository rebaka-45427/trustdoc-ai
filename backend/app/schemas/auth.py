from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ISSUER = "ISSUER"
    DOCUMENT_OWNER = "DOCUMENT_OWNER"
    REVIEWER = "REVIEWER"

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    # role is intentionally NOT accepted - always DOCUMENT_OWNER

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

class RefreshRequest(BaseModel):
    refresh_token: str
