import uuid
import os
import shutil
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.document import Document
from app.models.audit import AuditLog, IdSequence
from app.core.security import calculate_sha256, generate_doc_id, generate_chain_hash
from app.utils.helpers import validate_upload_file, ensure_upload_dir
from app.config import settings
from app.core.exceptions import NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB * 1024 * 1024

async def upload_document(db: Session, file: UploadFile, owner_id: str, upload_source: str = "OWNER_UPLOAD") -> Document:
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    if file_size > MAX_FILE_SIZE:
        raise ValidationError(f"File too large. Maximum allowed: {settings.MAX_FILE_SIZE_MB}MB")
    
    if file_size == 0:
        raise ValidationError("Empty file not allowed")
    
    # Validate file type
    safe_name, file_type = validate_upload_file(file)
    
    # Store file
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / safe_name
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Calculate SHA-256
    sha256 = calculate_sha256(str(file_path))
    
    # Generate sequential doc_id
    year = datetime.utcnow().year
    seq = get_next_sequence(db, "doc_id")
    doc_id = generate_doc_id(year, seq)
    
    # Create document record
    doc = Document(
        id=str(uuid.uuid4()),
        doc_id=doc_id,
        owner_id=owner_id,
        original_filename=file.filename,
        stored_filename=safe_name,
        file_path=str(file_path),
        file_type=file_type,
        file_size=file_size,
        sha256_hash=sha256,
        lifecycle_status="UPLOADED",
        ocr_status="PENDING",
        upload_source=upload_source,
        is_demo=False,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # Create audit log
    create_audit_event(db, "DOCUMENT_UPLOADED", owner_id, doc.id, {
        "doc_id": doc_id,
        "filename": file.filename,
        "sha256": sha256,
        "file_size": file_size,
    })
    
    return doc

def get_next_sequence(db: Session, sequence_name: str) -> int:
    seq = db.query(IdSequence).filter(IdSequence.name == sequence_name).with_for_update().first()
    if not seq:
        seq = IdSequence(name=sequence_name, current_value=0)
        db.add(seq)
    seq.current_value += 1
    db.commit()
    return seq.current_value

def create_audit_event(db: Session, event_type: str, actor_id: str, document_id: str, details: dict):
    # Get last audit event for chain
    last_event = db.query(AuditLog).order_by(AuditLog.created_at.desc()).first()
    prev_hash = last_event.current_event_hash if last_event else None
    
    event_data_str = f"{event_type}:{actor_id}:{document_id}:{str(details)}"
    current_hash = generate_chain_hash(prev_hash, event_data_str)
    
    audit = AuditLog(
        id=str(uuid.uuid4()),
        event_type=event_type,
        actor_id=actor_id,
        document_id=document_id,
        action_details=details,
        previous_event_hash=prev_hash,
        current_event_hash=current_hash,
    )
    db.add(audit)
    db.commit()
    return audit

def get_document_by_id(db: Session, doc_id: str, owner_id: str = None) -> Document:
    query = db.query(Document).filter(Document.id == doc_id)
    if owner_id:
        query = query.filter(Document.owner_id == owner_id)
    doc = query.first()
    if not doc:
        raise NotFoundError("Document not found")
    return doc
