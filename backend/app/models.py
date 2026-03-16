from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


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


class ViolationDetail(BaseModel):
    rule_code: str
    message: str


class BuildingEvaluation(BaseModel):
    building_id: str
    status: LegalityStatus
    confidence: float = Field(..., ge=0.0, le=1.0)
    violations: List[ViolationDetail] = []
    rule_version: str
    notes: Optional[str] = None
