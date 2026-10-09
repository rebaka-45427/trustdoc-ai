import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

get_password_hash = hash_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

def calculate_sha256(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def generate_hmac_token(data: str) -> str:
    return hmac.new(
        settings.HMAC_SECRET.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()

def generate_chain_hash(previous_hash: Optional[str], event_data: str) -> str:
    content = (previous_hash or "") + event_data
    return hashlib.sha256(content.encode()).hexdigest()

def generate_public_verification_id(year: int, sequence: int) -> str:
    return f"DV-{year}-{sequence:06d}"

def generate_doc_id(year: int, sequence: int) -> str:
    return f"DOC-{year}-{sequence:06d}"

def generate_review_case_id(year: int, sequence: int) -> str:
    return f"RC-{year}-{sequence:06d}"
