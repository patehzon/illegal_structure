from enum import Enum
from typing import List, Optional

from .compat import BaseModel, Field


class LegalityStatus(str, Enum):
    legal_today = "legal_today"
    illegal_today = "illegal_today"
    unknown_insufficient_data = "unknown_insufficient_data"
    non_conforming_tolerated = "non_conforming_tolerated"


class BuildingSummary(BaseModel):
    building_id: str = Field(..., description="Canonical building identifier")
    address: str
    arrondissement: int
    status: LegalityStatus
    confidence: float = Field(..., ge=0.0, le=1.0)
    rule_version: str


class ViolationDetail(BaseModel):
    rule_code: str
    severity: str
    message: str


class ExplanationDetail(BaseModel):
    rule_code: str
    outcome: str
    message: str


class BuildingEvaluation(BaseModel):
    building_id: str
    address: str
    arrondissement: int
    status: LegalityStatus
    confidence: float = Field(..., ge=0.0, le=1.0)
    violations: List[ViolationDetail] = Field(default_factory=list)
    explanations: List[ExplanationDetail] = Field(default_factory=list)
    missing_evidence: List[str] = Field(default_factory=list)
    rule_version: str
    notes: Optional[str] = None


class StatsResponse(BaseModel):
    total_buildings: int
    legal_today: int
    illegal_today: int
    unknown_insufficient_data: int
    non_conforming_tolerated: int
