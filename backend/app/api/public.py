from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.models.issuer import Issuer
from app.models.registration import RegistrationRecord
from app.models.public_verification import PublicVerificationEvent
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/public", tags=["Public Verification"])

@router.get("/verify/{public_verification_id}")
def public_verify(
    public_verification_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    # Find registered document
    doc = db.query(Document).filter(
        Document.public_verification_id == public_verification_id
    ).first()
    
    # Record verification attempt (anonymized)
    ip_hash = None
    client_ip = request.client.host if request.client else None
    if client_ip:
        import hashlib
        ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()[:16]
    
    if not doc:
        # Record failed attempt
        event = PublicVerificationEvent(
            id=str(uuid.uuid4()),
            document_id=None,
            verification_id_queried=public_verification_id,
            verifier_ip=ip_hash,
            user_agent=request.headers.get("user-agent", "")[:200],
            result="NOT_FOUND",
        )
        db.add(event)
        db.commit()
        return {
            "found": False,
            "message": "Document not found or not registered",
            "verification_id": public_verification_id,
        }
    
    result_type = "FOUND"
    if doc.lifecycle_status == "REVOKED":
        result_type = "REVOKED"
    
    # Record successful verification
    event = PublicVerificationEvent(
        id=str(uuid.uuid4()),
        document_id=str(doc.id),
        verification_id_queried=public_verification_id,
        verifier_ip=ip_hash,
        user_agent=request.headers.get("user-agent", "")[:200],
        result=result_type,
    )
    db.add(event)
    db.commit()
    
    # Fetch issuer info (safe public data only)
    issuer_info = None
    if doc.issuer_id:
        issuer = db.query(Issuer).filter(Issuer.id == str(doc.issuer_id)).first()
        if issuer:
            issuer_info = {
                "name": issuer.organization_name,
                "type": issuer.organization_type,
                "verified": issuer.verification_status == "VERIFIED",
            }
    
    # Get registration info
    reg = db.query(RegistrationRecord).filter(
        RegistrationRecord.document_id == str(doc.id)
    ).first()
    
    return {
        "found": True,
        "status": doc.lifecycle_status,
        "is_active": doc.lifecycle_status == "REGISTERED",
        "is_revoked": doc.lifecycle_status == "REVOKED",
        "verification_id": public_verification_id,
        "document_type": doc.document_type or "Document",
        "issuer": issuer_info,
        "registration_date": reg.registration_date.isoformat() if reg else None,
        "trust_score": doc.trust_score,
        "risk_level": doc.forensic_risk_level,
        "sha256_hash": doc.sha256_hash,
        "is_demo": doc.is_demo,
    }
