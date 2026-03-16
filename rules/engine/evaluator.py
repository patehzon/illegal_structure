from dataclasses import dataclass
from typing import Any


@dataclass
class EvaluationResult:
    status: str
    confidence: float
    violations: list[dict[str, str]]
    notes: str


def evaluate_building(building: dict[str, Any], rule_version: str = "2026-baseline") -> EvaluationResult:
    """Scaffold evaluator.

    Real implementation should execute spatial + attribute checks against
    rule catalog and produce fully explainable outputs.
    """

    required = ["height_m", "primary_use", "zone_code"]
    missing = [field for field in required if field not in building or building[field] is None]

    if missing:
        return EvaluationResult(
            status="unknown_insufficient_data",
            confidence=0.2,
            violations=[
                {
                    "rule_code": "DATA_MINIMUM_REQUIRED",
                    "message": f"Missing required fields: {', '.join(missing)}",
                }
            ],
            notes=f"Evaluated with ruleset {rule_version}.",
        )

    return EvaluationResult(
        status="legal_today",
        confidence=0.5,
        violations=[],
        notes=f"Scaffold positive result with ruleset {rule_version}; replace with full checks.",
    )
