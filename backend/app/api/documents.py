from fastapi import APIRouter, Depends, UploadFile, File, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.services.document_service import upload_document
from app.services.analysis_service import run_document_analysis, run_cross_document_analysis
from app.services.report_service import generate_pdf_report, generate_qr_code
from app.models.user import User
from app.models.document import Document
from app.models.audit import AuditLog
from app.models.registration import RegistrationRecord
from app.schemas.document import RevokeRequest
import os
import uuid
from datetime import datetime
from app.config import settings

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/upload")
async def upload_doc(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["DOCUMENT_OWNER", "ISSUER", "ADMIN"]))
):
    upload_source = "ISSUER_UPLOAD" if current_user.role == "ISSUER" else "OWNER_UPLOAD"
    doc = await upload_document(db, file, str(current_user.id), upload_source)
    return {"message": "Document uploaded successfully", "doc_id": doc.doc_id, "id": doc.id}

@router.get("")
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    docs = db.query(Document).filter(Document.owner_id == str(current_user.id)).all()
    return {"documents": [{"id": str(d.id), "doc_id": d.doc_id, "status": d.lifecycle_status} for d in docs]}

@router.post("/{doc_id}/analyze")
def start_analysis(doc_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    doc.lifecycle_status = "ANALYZING"
    db.commit()
    background_tasks.add_task(run_document_analysis, db, doc_id)
    return {"message": "Analysis started", "doc_id": doc.doc_id}

@router.get("/{doc_id}/analysis")
def get_analysis(doc_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    return {
        "doc_id": doc.doc_id,
        "lifecycle_status": doc.lifecycle_status,
        "document_type": doc.document_type,
        "trust_score": doc.trust_score,
        "forensic_risk_level": doc.forensic_risk_level
    }

@router.get("/cross-check")
def cross_check(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return run_cross_document_analysis(db, str(current_user.id))

@router.get("/{doc_id}/report")
def get_report(doc_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc: return {"error": "Not found"}
    report_path = os.path.join(settings.REPORTS_DIR, f"{doc.doc_id}_report.pdf")
    generate_pdf_report({"Document ID": doc.doc_id, "Trust Score": doc.trust_score}, report_path)
    return {"report_url": f"/reports/{os.path.basename(report_path)}"}
