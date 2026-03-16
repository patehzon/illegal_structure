from fastapi import FastAPI, Query

from .models import BuildingEvaluation, BuildingSummary, LegalityStatus, ViolationDetail

app = FastAPI(title="Illegal Structure API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/buildings", response_model=list[BuildingSummary])
def list_buildings(
    min_arr: int = Query(default=1, ge=1, le=20),
    max_arr: int = Query(default=20, ge=1, le=20),
) -> list[BuildingSummary]:
    demo_data = [
        BuildingSummary(
            building_id="PARIS-DEMO-0001",
            address="10 Rue de Rivoli",
            arrondissement=1,
            status=LegalityStatus.unknown_insufficient_data,
        )
    ]
    return [b for b in demo_data if min_arr <= b.arrondissement <= max_arr]


@app.get("/v1/buildings/{building_id}", response_model=BuildingEvaluation)
def get_building(building_id: str) -> BuildingEvaluation:
    return BuildingEvaluation(
        building_id=building_id,
        status=LegalityStatus.unknown_insufficient_data,
        confidence=0.25,
        violations=[
            ViolationDetail(
                rule_code="DATA_MISSING_HEIGHT",
                message="Height information is missing; cannot fully evaluate envelope compliance.",
            )
        ],
        rule_version="2026-baseline",
        notes="Scaffold response. Replace with real rule-engine output.",
    )


@app.get("/v1/stats")
def get_stats() -> dict[str, int]:
    return {
        "total_buildings": 1,
        "legal_today": 0,
        "illegal_today": 0,
        "unknown_insufficient_data": 1,
        "non_conforming_tolerated": 0,
    }
