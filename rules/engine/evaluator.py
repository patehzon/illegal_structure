import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any


@dataclass
class Violation:
    rule_code: str
    severity: str
    message: str


@dataclass
class Explanation:
    rule_code: str
    outcome: str
    message: str


@dataclass
class EvaluationResult:
    status: str
    confidence: float
    rule_version: str
    violations: list[Violation] = field(default_factory=list)
    explanations: list[Explanation] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    notes: str = ""


CATALOG_DIR = Path(__file__).resolve().parents[1] / "catalog"


@lru_cache(maxsize=None)
def load_rule_catalog(rule_version: str = "2026-baseline") -> dict[str, Any]:
    catalog_path = CATALOG_DIR / f"{rule_version}.yaml"
    if not catalog_path.exists():
        raise ValueError(f"Unknown rule catalog: {rule_version}")
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def _rule_metadata(catalog: dict[str, Any]) -> dict[str, dict[str, str]]:
    return {rule["code"]: rule for rule in catalog["rules"]}


def _missing_required_fields(building: dict[str, Any], required_fields: list[str]) -> list[str]:
    missing = []
    for field_name in required_fields:
        value = building.get(field_name)
        if value is None:
            missing.append(field_name)
            continue
        if isinstance(value, str) and not value.strip():
            missing.append(field_name)
    return missing


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def evaluate_building(building: dict[str, Any], rule_version: str = "2026-baseline") -> EvaluationResult:
    catalog = load_rule_catalog(rule_version)
    rules = _rule_metadata(catalog)
    missing = _missing_required_fields(building, catalog["required_fields"])

    if missing:
        message = f"Missing required fields: {', '.join(missing)}"
        return EvaluationResult(
            status="unknown_insufficient_data",
            confidence=0.2,
            rule_version=catalog["version"],
            violations=[
                Violation(
                    rule_code="DATA_MINIMUM_REQUIRED",
                    severity=rules["DATA_MINIMUM_REQUIRED"]["severity"],
                    message=message,
                )
            ],
            explanations=[
                Explanation(
                    rule_code="DATA_MINIMUM_REQUIRED",
                    outcome="fail",
                    message=message,
                )
            ],
            missing_evidence=missing,
            notes=f"Evaluated with ruleset {catalog['version']}.",
        )

    zone_code = str(building["zone_code"]).upper()
    zone = catalog["zones"].get(zone_code)
    if zone is None:
        message = f"Zone code '{zone_code}' is not mapped in the local rules catalog."
        return EvaluationResult(
            status="unknown_insufficient_data",
            confidence=0.25,
            rule_version=catalog["version"],
            violations=[
                Violation(
                    rule_code="ZONE_CODE_UNMAPPED",
                    severity=rules["ZONE_CODE_UNMAPPED"]["severity"],
                    message=message,
                )
            ],
            explanations=[
                Explanation(
                    rule_code="ZONE_CODE_UNMAPPED",
                    outcome="fail",
                    message=message,
                )
            ],
            missing_evidence=[f"zone_mapping:{zone_code}"],
            notes="Catalog coverage is incomplete for this zone code.",
        )

    explanations: list[Explanation] = []
    violations: list[Violation] = []
    allowed_uses = {allowed_use.lower() for allowed_use in zone["allowed_uses"]}
    primary_use = str(building["primary_use"]).lower()
    if primary_use in allowed_uses:
        explanations.append(
            Explanation(
                rule_code="LAND_USE_COMPATIBILITY",
                outcome="pass",
                message=f"Use '{primary_use}' is allowed in zone {zone_code}.",
            )
        )
    else:
        violations.append(
            Violation(
                rule_code="LAND_USE_COMPATIBILITY",
                severity=rules["LAND_USE_COMPATIBILITY"]["severity"],
                message=f"Use '{primary_use}' is not allowed in zone {zone_code}.",
            )
        )
        explanations.append(
            Explanation(
                rule_code="LAND_USE_COMPATIBILITY",
                outcome="fail",
                message=f"Use '{primary_use}' is not allowed in zone {zone_code}.",
            )
        )

    max_height_m = _as_float(zone["max_height_m"])
    height_m = _as_float(building["height_m"])
    if height_m is None or max_height_m is None:
        message = "Height evidence is not usable for comparison."
        return EvaluationResult(
            status="unknown_insufficient_data",
            confidence=0.2,
            rule_version=catalog["version"],
            violations=[
                Violation(
                    rule_code="DATA_MINIMUM_REQUIRED",
                    severity=rules["DATA_MINIMUM_REQUIRED"]["severity"],
                    message=message,
                )
            ],
            explanations=explanations
            + [
                Explanation(
                    rule_code="HEIGHT_MAX_BY_ZONE",
                    outcome="fail",
                    message=message,
                )
            ],
            missing_evidence=["height_m"],
            notes="Height must be numeric for rule evaluation.",
        )
    if height_m <= max_height_m:
        explanations.append(
            Explanation(
                rule_code="HEIGHT_MAX_BY_ZONE",
                outcome="pass",
                message=f"Height {height_m:.1f}m is within the {max_height_m:.1f}m limit for zone {zone_code}.",
            )
        )
    else:
        violations.append(
            Violation(
                rule_code="HEIGHT_MAX_BY_ZONE",
                severity=rules["HEIGHT_MAX_BY_ZONE"]["severity"],
                message=f"Height {height_m:.1f}m exceeds the {max_height_m:.1f}m limit for zone {zone_code}.",
            )
        )
        explanations.append(
            Explanation(
                rule_code="HEIGHT_MAX_BY_ZONE",
                outcome="fail",
                message=f"Height {height_m:.1f}m exceeds the {max_height_m:.1f}m limit for zone {zone_code}.",
            )
        )

    heritage_message = catalog["heritage"]["message"]
    if building.get("heritage_protected"):
        explanations.append(
            Explanation(
                rule_code="HERITAGE_OVERRIDE",
                outcome="unknown",
                message=heritage_message,
            )
        )
    else:
        explanations.append(
            Explanation(
                rule_code="HERITAGE_OVERRIDE",
                outcome="pass",
                message="No heritage-protection flag is present in the MVP evidence bundle.",
            )
        )

    if violations:
        return EvaluationResult(
            status="illegal_today",
            confidence=0.9,
            rule_version=catalog["version"],
            violations=violations,
            explanations=explanations,
            notes=f"Evaluated with ruleset {catalog['version']}.",
        )

    if building.get("heritage_protected"):
        return EvaluationResult(
            status="unknown_insufficient_data",
            confidence=0.45,
            rule_version=catalog["version"],
            violations=[
                Violation(
                    rule_code="HERITAGE_OVERRIDE",
                    severity=rules["HERITAGE_OVERRIDE"]["severity"],
                    message=heritage_message,
                )
            ],
            explanations=explanations,
            missing_evidence=[catalog["heritage"]["manual_review_missing_evidence"]],
            notes="Base zoning checks pass, but heritage review remains unresolved in the MVP.",
        )

    return EvaluationResult(
        status="legal_today",
        confidence=0.95,
        rule_version=catalog["version"],
        violations=[],
        explanations=explanations,
        notes=f"Evaluated with ruleset {catalog['version']}.",
    )
