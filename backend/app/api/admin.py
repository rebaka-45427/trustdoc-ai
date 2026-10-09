from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User
from app.models.document import Document
from app.models.issuer import Issuer
from app.models.review import ReviewCase
from app.models.audit import AuditLog
from app.models.registration import RegistrationRecord
from app.schemas.user import UserUpdateRequest, CreateUserRequest
from app.core.security import hash_password, generate_public_verification_id, generate_hmac_token, generate_doc_id
from app.services.document_service import get_next_sequence, create_audit_event
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    users = db.query(User).all()
    return [user_to_dict(u) for u in users]

@router.post("/users")
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    valid_roles = ["ADMIN", "ISSUER", "DOCUMENT_OWNER", "REVIEWER"]
    if request.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Valid: {valid_roles}")
    
    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        hashed_password=hash_password(request.password),
        full_name=request.full_name,
        role=request.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_to_dict(user)

@router.patch("/users/{user_id}")
def update_user(
    user_id: str,
    request: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if request.role:
        valid_roles = ["ADMIN", "ISSUER", "DOCUMENT_OWNER", "REVIEWER"]
        if request.role not in valid_roles:
            raise HTTPException(status_code=400, detail="Invalid role")
        user.role = request.role
    if request.is_active is not None:
        user.is_active = request.is_active
    if request.full_name:
        user.full_name = request.full_name
    db.commit()
    return user_to_dict(user)

@router.get("/documents")
def list_all_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    docs = db.query(Document).order_by(Document.created_at.desc()).limit(100).all()
    return [doc_to_dict(d) for d in docs]

@router.post("/documents/{doc_id}/register")
def register_document(
    doc_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if doc.lifecycle_status not in ["APPROVED", "ANALYZED", "ISSUER_VERIFIED"]:
        raise HTTPException(status_code=400, detail=f"Document must be APPROVED before registration. Current: {doc.lifecycle_status}")
    
    if doc.sha256_hash is None:
        raise HTTPException(status_code=400, detail="Document must have SHA-256 hash")
    
    # Generate public verification ID
    year = datetime.utcnow().year
    seq = get_next_sequence(db, "pub_verify_id")
    pub_id = generate_public_verification_id(year, seq)
    hmac_token = generate_hmac_token(pub_id)
    
    # Update document
    doc.lifecycle_status = "REGISTERED"
    doc.public_verification_id = pub_id
    doc.hmac_token = hmac_token
    doc.updated_at = datetime.utcnow()
    
    # Create registration record
    reg = RegistrationRecord(
        id=str(uuid.uuid4()),
        document_id=doc_id,
        registered_by=str(current_user.id),
        public_verification_id=pub_id,
        hmac_token=hmac_token,
        registration_date=datetime.utcnow(),
        is_active=True,
    )
    db.add(reg)
    db.commit()
    
    create_audit_event(db, "DOCUMENT_REGISTERED", str(current_user.id), doc_id, {
        "public_verification_id": pub_id,
    })
    
    return {
        "message": "Document registered successfully",
        "public_verification_id": pub_id,
        "verify_url": f"{__import__('app.config', fromlist=['settings']).settings.PUBLIC_BASE_URL}/verify/{pub_id}",
    }

@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    total_docs = db.query(func.count(Document.id)).scalar()
    registered = db.query(func.count(Document.id)).filter(Document.lifecycle_status == "REGISTERED").scalar()
    pending_review = db.query(func.count(Document.id)).filter(Document.lifecycle_status == "IN_REVIEW").scalar()
    revoked = db.query(func.count(Document.id)).filter(Document.lifecycle_status == "REVOKED").scalar()
    total_users = db.query(func.count(User.id)).scalar()
    total_issuers = db.query(func.count(Issuer.id)).scalar()
    verified_issuers = db.query(func.count(Issuer.id)).filter(Issuer.verification_status == "VERIFIED").scalar()
    
    return {
        "documents": {
            "total": total_docs,
            "registered": registered,
            "pending_review": pending_review,
            "revoked": revoked,
        },
        "users": {"total": total_users},
        "issuers": {"total": total_issuers, "verified": verified_issuers},
    }

@router.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return [
        {
            "id": str(l.id),
            "event_type": l.event_type,
            "actor_id": str(l.actor_id) if l.actor_id else None,
            "document_id": str(l.document_id) if l.document_id else None,
            "details": l.action_details,
            "hash": l.current_event_hash,
            "created_at": l.created_at.isoformat(),
        }
        for l in logs
    ]

def user_to_dict(user: User) -> dict:
    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
    }

def doc_to_dict(doc: Document) -> dict:
    return {
        "id": str(doc.id),
        "doc_id": doc.doc_id,
        "public_verification_id": doc.public_verification_id,
        "original_filename": doc.original_filename,
        "file_type": doc.file_type,
        "lifecycle_status": doc.lifecycle_status,
        "trust_score": doc.trust_score,
        "is_demo": doc.is_demo,
        "created_at": doc.created_at.isoformat(),
    }
