from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.api import auth, documents, issuers, reviews, admin, public
import os

app = FastAPI(
    title="TrustDoc AI API",
    description="AI-Powered Digital Document Provenance, Forensic Verification & Trust Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(issuers.router)
app.include_router(reviews.router)
app.include_router(admin.router)
app.include_router(public.router)

from app.database import engine, Base

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    try:
        from app.database import SessionLocal
        from app.models.user import User, UserRole
        from app.core.security import hash_password
        
        db = SessionLocal()
        admin_email = "admin@trustdoc.ai"
        if not db.query(User).filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                hashed_password=hash_password("Admin@123456"),
                full_name="System Admin",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            
        reviewer_email = "reviewer@trustdoc.ai"
        if not db.query(User).filter_by(email=reviewer_email).first():
            reviewer = User(
                email=reviewer_email,
                hashed_password=hash_password("Review@123456"),
                full_name="System Reviewer",
                role=UserRole.REVIEWER,
                is_active=True
            )
            db.add(reviewer)
            
        db.commit()
        db.close()
        print("Database initialized and seeded successfully!")
    except Exception as e:
        print(f"Database seed note: {e}")

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
os.makedirs(frontend_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "TrustDoc AI API", "version": "1.0.0"}
