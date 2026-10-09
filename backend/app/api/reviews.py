from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.review import ReviewCase
from app.models.document import Document
from app.models.user import User
from app.schemas.review import ReviewDecisionRequest
from app.services.document_service import get_next_sequence
from app.core.security import generate_review_case_id
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

@router.get("")
def list_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["REVIEWER", "ADMIN"]))
):
    query = db.query(ReviewCase)
    if current_user.role == "REVIEWER":
        query = query.filter(ReviewCase.reviewer_id == str(current_user.id))
    cases = query.order_by(ReviewCase.created_at.desc()).all()
    return [review_to_dict(r) for r in cases]

@router.post("/{review_id}/assign")
def assign_reviewer(
    review_id: str,
    reviewer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    case = db.query(ReviewCase).filter(ReviewCase.id == review_id).first()
    if not case:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Review case not found")
    reviewer = db.query(User).filter(User.id == reviewer_id, User.role == "REVIEWER").first()
    if not reviewer:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Reviewer not found")
    case.reviewer_id = reviewer_id
    case.status = "IN_REVIEW"
    db.commit()
    return review_to_dict(case)

@router.patch("/{review_id}/decision")
def submit_decision(
    review_id: str,
    request: ReviewDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["REVIEWER", "ADMIN"]))
):
    case = db.query(ReviewCase).filter(ReviewCase.id == review_id).first()
    if not case:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Review case not found")
    if current_user.role == "REVIEWER" and str(case.reviewer_id) != str(current_user.id):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not assigned to this review")
    
    if request.decision == "OVERRIDE_FINDING" and not request.override_reason:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Override reason is required when overriding a finding")
    
    case.decision = request.decision
    case.reason = request.reason
    case.override_reason = request.override_reason
    case.reviewed_at = datetime.utcnow()
    
    if request.decision == "APPROVE" or request.decision == "OVERRIDE_FINDING":
        case.status = "APPROVED"
        doc = db.query(Document).filter(Document.id == str(case.document_id)).first()
        if doc:
            doc.lifecycle_status = "APPROVED"
            doc.updated_at = datetime.utcnow()
    elif request.decision == "REJECT":
        case.status = "REJECTED"
        doc = db.query(Document).filter(Document.id == str(case.document_id)).first()
        if doc:
            doc.lifecycle_status = "REJECTED"
            doc.updated_at = datetime.utcnow()
    
    db.commit()
    return review_to_dict(case)

def review_to_dict(case: ReviewCase) -> dict:
    return {
        "id": str(case.id),
        "review_case_id": case.review_case_id,
        "document_id": str(case.document_id),
        "reviewer_id": str(case.reviewer_id) if case.reviewer_id else None,
        "status": case.status,
        "decision": case.decision,
        "reason": case.reason,
        "created_at": case.created_at.isoformat(),
        "reviewed_at": case.reviewed_at.isoformat() if case.reviewed_at else None,
    }
