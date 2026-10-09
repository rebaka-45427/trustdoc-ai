# TrustDoc AI Project Guide

A complete guide to the modules implemented in TrustDoc AI:

1. **Authentication**: JWT-based RBAC.
2. **Document Upload**: Secure SHA-256 fingerprinting on upload.
3. **AI Pipeline**: 
   - **OCR**: Extracts fields automatically.
   - **Forensics**: Analyzes images for inconsistencies (simulated via AI scripts).
4. **Trust Scoring**: Algorithms weigh OCR, integrity, and cross-checks to yield a 0-100 score.
5. **Cross-Document Analysis**: Identity resolution checks multiple docs for mismatched timelines.
6. **Registration**: Secures approved documents.
7. **QR Generation**: Produces a public scan link.
8. **Audit Trail**: Hash-chained events prevent log tampering.

*Read `PROJECT_EXPLANATION.md` for more details.*
