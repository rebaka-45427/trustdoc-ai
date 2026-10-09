# TrustDoc AI - Viva Guide

**Q: What is your project?**
A: TrustDoc AI is a smart platform for verifying documents using AI to detect tampering and generating secure QR codes for instant verification.

**Q: What problem does it solve?**
A: It eliminates manual background checks by instantly verifying documents and finding fake certificates.

**Q: How does OCR work?**
A: We use optical character recognition (like PyTesseract) to convert document images into readable text and extract key fields like Name and DOB.

**Q: How do you detect tampering?**
A: We use Error Level Analysis (ELA) and noise pattern detection. If someone Photoshops a name, the compressed edges of those pixels look different under AI.

**Q: What is SHA-256?**
A: It is a cryptographic algorithm that creates a unique digital fingerprint for a file. If even one pixel changes, the hash completely changes.

**Q: What is the Trust Score?**
A: A 0-100 score combining the results of OCR clarity, forensic integrity, and issuer verification.

**Q: What is the Risk Score?**
A: A measure of the likelihood that the document was forged, based purely on image artifacts and metadata.

**Q: How does QR verification work?**
A: Once a document is fully approved and registered, the system generates a secure URL and embeds it in a QR code. Scanning it opens a public verification page.

**Q: What happens if two documents contain different DOBs?**
A: Our Cross-Document Intelligence module flags a "TIMELINE INCONSISTENCY" and sends the profile for manual review.

**Q: How does your system protect personal information?**
A: Public QR pages only show masked info and verification status, not private numbers (like Aadhaar/PAN).
