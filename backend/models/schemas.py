from typing import List, Optional
from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None


class Claim(BaseModel):
    claim: str
    importance: float = Field(default=1.0, ge=0.0, le=1.0)


class Evidence(BaseModel):
    title: str
    url: str
    snippet: str
    source_domain: str
    source_score: float


class ClaimResult(BaseModel):
    claim: str
    verdict: str
    confidence: float
    explanation: str
    evidence: List[Evidence]


class VerificationResponse(BaseModel):
    input_text: str
    overall_verdict: str
    overall_confidence: float
    claims: List[ClaimResult]