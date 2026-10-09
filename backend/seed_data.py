import os
import sys

# Seed script stub that can be extended
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    admin_email = "admin@trustdoc.ai"
    if not db.query(User).filter_by(email=admin_email).first():
        admin = User(
            email=admin_email,
            hashed_password=get_password_hash("Admin@123456"),
            full_name="System Admin",
            role=UserRole.ADMIN
        )
        db.add(admin)
        
    reviewer_email = "reviewer@trustdoc.ai"
    if not db.query(User).filter_by(email=reviewer_email).first():
        reviewer = User(
            email=reviewer_email,
            hashed_password=get_password_hash("Review@123456"),
            full_name="System Reviewer",
            role=UserRole.REVIEWER
        )
        db.add(reviewer)
        
    db.commit()
    db.close()
    print("Database seeded with Admin and Reviewer accounts!")

if __name__ == "__main__":
    seed_db()
