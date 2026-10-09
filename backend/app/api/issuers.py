from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.issuer import Issuer
from app.models.user import User
from app.schemas.issuer import IssuerCreateRequest, IssuerVerifyRequest
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/issuers", tags=["Issuers"])

@router.post("")
def create_issuer(
    request: IssuerCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    issuer = Issuer(
        id=str(uuid.uuid4()),
        organization_name=request.organization_name,
        organization_type=request.organization_type,
        official_domain=request.official_domain,
        official_email=request.official_email,
        registration_reference=request.registration_reference,
        verification_status="PENDING",
        is_demo=request.is_demo,
    )
    db.add(issuer)
    db.commit()
    db.refresh(issuer)
    return issuer_to_dict(issuer)

@router.get("")
def list_issuers(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "ISSUER", "REVIEWER"]))
):
    issuers = db.query(Issuer).all()
    return [issuer_to_dict(i) for i in issuers]

@router.get("/{issuer_id}")
def get_issuer(
    issuer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issuer = db.query(Issuer).filter(Issuer.id == issuer_id).first()
    if not issuer:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Issuer not found")
    return issuer_to_dict(issuer)

@router.patch("/{issuer_id}/verify")
def verify_issuer(
    issuer_id: str,
    request: IssuerVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    issuer = db.query(Issuer).filter(Issuer.id == issuer_id).first()
    if not issuer:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Issuer not found")
    issuer.verification_status = "VERIFIED"
    issuer.verified_at = datetime.utcnow()
    issuer.verified_by = str(current_user.id)
    db.commit()
    db.refresh(issuer)
    return issuer_to_dict(issuer)

@router.patch("/{issuer_id}/suspend")
def suspend_issuer(
    issuer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    issuer = db.query(Issuer).filter(Issuer.id == issuer_id).first()
    if not issuer:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Issuer not found")
    issuer.verification_status = "SUSPENDED"
    db.commit()
    db.refresh(issuer)
    return issuer_to_dict(issuer)

def issuer_to_dict(issuer: Issuer) -> dict:
    return {
        "id": str(issuer.id),
        "organization_name": issuer.organization_name,
        "organization_type": issuer.organization_type,
        "official_domain": issuer.official_domain,
        "official_email": issuer.official_email,
        "registration_reference": issuer.registration_reference,
        "verification_status": issuer.verification_status,
        "verified_at": issuer.verified_at.isoformat() if issuer.verified_at else None,
        "is_demo": issuer.is_demo,
        "created_at": issuer.created_at.isoformat(),
    }
