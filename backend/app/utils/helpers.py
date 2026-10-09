import os
import uuid
import mimetypes
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_MIME_TYPES = {
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
}

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

def validate_upload_file(file: UploadFile) -> Tuple[str, str]:
    """Validate file type, extension, and return (safe_filename, file_type)"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File extension not allowed. Allowed: {ALLOWED_EXTENSIONS}")
    
    content_type = file.content_type or ""
    if content_type not in ALLOWED_MIME_TYPES and content_type != "application/octet-stream":
        # Be lenient with content type but strict with extension
        pass
    
    safe_name = f"{uuid.uuid4()}.{ext}"
    file_type = ext.upper()
    if file_type == "JPG":
        file_type = "JPG"
    return safe_name, file_type

def ensure_upload_dir() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

def ensure_reports_dir() -> Path:
    reports_dir = Path(settings.REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir

def get_file_size_mb(size_bytes: int) -> float:
    return size_bytes / (1024 * 1024)

def mask_sensitive_data(value: str, show_chars: int = 4) -> str:
    if not value or len(value) <= show_chars:
        return "***"
    return value[:show_chars] + "*" * (len(value) - show_chars)
