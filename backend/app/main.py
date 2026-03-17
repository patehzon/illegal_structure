from rules.engine.evaluator import evaluate_building

from .compat import CORSMiddleware, FastAPI, HTTPException, Query
from .data import get_demo_building, list_demo_buildings
from .models import (
    BuildingEvaluation,
    BuildingSummary,
    ExplanationDetail,
    StatsResponse,
    ViolationDetail,
)

app = FastAPI(title="Illegal Structure API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _in_arrondissement_range(building: dict[str, object], min_arr: int, max_arr: int) -> bool:
    arrondissement = int(building["arrondissement"])
    return min_arr <= arrondissement <= max_arr


def _normalize_int_query_value(value: object) -> int:
    return int(getattr(value, "default", value))


def _build_summary(building: dict[str, object]) -> BuildingSummary:
    evaluation = evaluate_building(building)
    return BuildingSummary(
        building_id=str(building["building_id"]),
        address=str(building["address"]),
        arrondissement=int(building["arrondissement"]),
        status=evaluation.status,
        confidence=evaluation.confidence,
        rule_version=evaluation.rule_version,
    )


def _build_evaluation(building: dict[str, object]) -> BuildingEvaluation:
    evaluation = evaluate_building(building)
    return BuildingEvaluation(
        building_id=str(building["building_id"]),
        address=str(building["address"]),
        arrondissement=int(building["arrondissement"]),
        status=evaluation.status,
        confidence=evaluation.confidence,
        violations=[
            ViolationDetail(
                rule_code=violation.rule_code,
                severity=violation.severity,
                message=violation.message,
            )
            for violation in evaluation.violations
        ],
        explanations=[
            ExplanationDetail(
                rule_code=explanation.rule_code,
                outcome=explanation.outcome,
                message=explanation.message,
            )
            for explanation in evaluation.explanations
        ],
        missing_evidence=evaluation.missing_evidence,
        rule_version=evaluation.rule_version,
        notes=evaluation.notes,
    )


@app.get("/v1/buildings", response_model=list[BuildingSummary])
def list_buildings(
    min_arr: int = Query(default=1, ge=1, le=20),
    max_arr: int = Query(default=20, ge=1, le=20),
) -> list[BuildingSummary]:
    min_arr = _normalize_int_query_value(min_arr)
    max_arr = _normalize_int_query_value(max_arr)
    return [
        _build_summary(building)
        for building in list_demo_buildings()
        if _in_arrondissement_range(building, min_arr, max_arr)
    ]


@app.get("/v1/buildings/{building_id}", response_model=BuildingEvaluation)
def get_building(building_id: str) -> BuildingEvaluation:
    building = get_demo_building(building_id)
    if building is None:
        raise HTTPException(status_code=404, detail=f"Unknown building_id '{building_id}'")
    return _build_evaluation(building)


@app.get("/v1/stats", response_model=StatsResponse)
def get_stats(
    min_arr: int = Query(default=1, ge=1, le=20),
    max_arr: int = Query(default=20, ge=1, le=20),
) -> StatsResponse:
    min_arr = _normalize_int_query_value(min_arr)
    max_arr = _normalize_int_query_value(max_arr)
    summaries = [
        _build_summary(building)
        for building in list_demo_buildings()
        if _in_arrondissement_range(building, min_arr, max_arr)
    ]
    counts = {
        "total_buildings": len(summaries),
        "legal_today": 0,
        "illegal_today": 0,
        "unknown_insufficient_data": 0,
        "non_conforming_tolerated": 0,
    }
    for summary in summaries:
        counts[summary.status] += 1
    return StatsResponse(**counts)
