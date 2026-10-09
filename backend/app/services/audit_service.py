from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from typing import Optional, List

def get_audit_logs(db: Session, document_id: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[AuditLog]:
    query = db.query(AuditLog)
    if document_id:
        query = query.filter(AuditLog.document_id == document_id)
    return query.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()
