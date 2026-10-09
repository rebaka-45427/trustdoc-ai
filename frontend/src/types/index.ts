export type Role = 'ADMIN' | 'ISSUER' | 'DOCUMENT_OWNER' | 'REVIEWER';

export interface User {
  id: string;
  email: string;
  fullName: string;
  role: Role;
}

export type DocumentStatus = 'PENDING' | 'REGISTERED' | 'SUSPICIOUS' | 'REVOKED';
export type FileType = 'PDF' | 'JPG' | 'JPEG' | 'PNG';

export interface Document {
  id: string;
  title: string;
  type: FileType;
  status: DocumentStatus;
  trustScore: number;
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  sha256: string;
  createdAt: string;
  issuerId?: string;
  ownerId: string;
}

export type IssuerStatus = 'ACTIVE' | 'SUSPENDED' | 'REVOKED';

export interface Issuer {
  id: string;
  name: string;
  publicKey: string;
  status: IssuerStatus;
  createdAt: string;
}

export interface ReviewCase {
  id: string;
  documentId: string;
  reviewerId?: string;
  status: 'OPEN' | 'IN_PROGRESS' | 'RESOLVED';
  notes: string;
  createdAt: string;
}

export interface ProvenanceEvent {
  id: string;
  documentId: string;
  eventType: string;
  actorId: string;
  timestamp: string;
  details: string;
}

export interface AuditLog {
  id: string;
  action: string;
  userId: string;
  timestamp: string;
  details: string;
}

export interface TrustScore {
  score: number;
  factors: { name: string; impact: number }[];
}

export interface RiskScore {
  level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  score: number;
  reasons: string[];
}

export interface ForensicAnalysis {
  id: string;
  documentId: string;
  metadataTampering: boolean;
  pixelInconsistencies: boolean;
  fontsMatched: boolean;
  score: number;
}

export interface ExtractedData {
  [key: string]: any;
}

export interface AnalyticsData {
  totalDocuments: number;
  totalUsers: number;
  suspiciousDocuments: number;
  pendingReviews: number;
}

export interface PublicVerificationResult {
  isRegistered: boolean;
  isActive: boolean;
  document?: Document;
  issuer?: Issuer;
  message: string;
}
