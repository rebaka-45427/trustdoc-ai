# TrustDoc AI - Complete Explanation Guide

## 1. Project Title
**TrustDoc AI**: AI-Powered Digital Document Provenance, Verification & Forensic Intelligence Platform.

## 2. Problem Statement
Fake documents, forged certificates, and tampered identities are increasing. Traditional verification methods are slow, manual, and prone to human error, allowing fraudulent documents to bypass background checks.

## 3. Existing System
Currently, background verification requires calling universities, sending emails, or manually inspecting documents. 

## 4. Problems with Existing Systems
- Takes 2 to 4 weeks.
- Highly expensive.
- Manual checks miss advanced digital tampering (Photoshop).
- No cross-document correlation.

## 5. Proposed System
TrustDoc AI introduces a unified verification pipeline combining OCR, AI forensics, and cryptographic registration to instantly analyze and issue verifiable QR codes.

## 6. Why Our Project is Different
Unlike standard digi-lockers, TrustDoc actively runs forensic tests (Error Level Analysis) and cross-references data across multiple documents for timeline inconsistencies.

## 7. Main Features
- **OCR & Extraction**: Pulls fields automatically.
- **AI Forensics**: Detects Photoshop and tampering.
- **Cross-Document Analysis**: Finds mismatching DOBs across files.
- **Cryptographic Registration**: Immutably registers verified documents with SHA-256.
- **Instant QR Verification**: Scan to verify without login.

## 8. Technology Stack
- **Backend**: FastAPI, Python, SQLAlchemy, PostgreSQL.
- **AI/ML**: OpenCV, Scikit-learn, PyTesseract, Pillow.
- **Frontend**: React (Vercel ready).

## 9. Architecture
1. **Upload** -> 2. **AI Pipeline** (OCR + Forensics) -> 3. **Review/Issuer Gate** -> 4. **Registration** -> 5. **QR Code**.

## 10. Database Design
PostgreSQL with hash-chained tables for Audit logs, guaranteeing immutability.

*(Full explanations of OCR, SHA-256, Forensics, and Trust Score are detailed in VIVA_GUIDE.md)*
