# API Documentation

TrustDoc AI is powered by a comprehensive FastAPI backend. You can access the interactive Swagger UI at `/docs` when the server is running.

## Core Endpoints

### Authentication
- `POST /api/auth/register`: Register a new document owner.
- `POST /api/auth/login`: Authenticate and receive a JWT access token.
- `GET /api/auth/me`: Get current user details.

### Documents
- `POST /api/documents/upload`: Upload a document, generates SHA-256 and initial DB record.
- `GET /api/documents`: List user's documents.
- `POST /api/documents/{id}/analyze`: Triggers OCR, extraction, and forensic risk evaluation.
- `GET /api/documents/cross-check`: Evaluates timeline consistency across the user's uploaded documents.
- `GET /api/documents/{id}/report`: Generates a PDF verification report.
- `POST /api/documents/{id}/revoke`: Revokes a document (requires Admin/Issuer).

### Issuers & Review Workflow
- `POST /api/issuers`: Create a new issuer.
- `PATCH /api/issuers/{id}/verify`: Verify an issuer.
- `POST /api/reviews/{id}/decision`: Approve or reject a document with a recorded decision.

### Public Verification
- `GET /api/public/verify/{publicVerificationId}`: Returns safe, sanitized data for a registered document. Designed for unauthenticated access via QR code scanning.

## Access Control
Most endpoints require a valid `Authorization: Bearer <token>` header. Public endpoints (`/api/public/*`) are completely open.
