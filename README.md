# Illegal Structure — Paris Building Legality (2026)

This repository scaffolds a full-stack geospatial system to:

1. Build a **comprehensive inventory of existing buildings in Paris**.
2. Evaluate whether each building would be **legal if built today (2026)**.
3. Visualize results **building-by-building, street-by-street** on an interactive map.
4. Provide a dashboard with aggregate statistics and explainability.

## Monorepo structure

- `backend/` — FastAPI service for query + evaluation APIs.
- `etl/` — ingestion/normalization pipeline for building and regulation data.
- `rules/` — versioned legality rules and evaluation engine.
- `frontend/` — React + Leaflet map and dashboard scaffold.
- `infra/` — docker-compose and local environment utilities.
- `docs/` — methodology, governance, assumptions, and data lineage.

## Quick start (scaffold)

```bash
cp .env.example .env
make bootstrap
make check
```

## What is implemented now

- Base directory scaffold and coding entry points.
- Backend API with health, building list/detail, and stats endpoints backed by the evaluator.
- Rule catalog and evaluator for MVP zone/use/height checks with explainability fields.
- Runnable ETL staging skeleton with provenance-rich manifest and JSONL outputs.
- Frontend React dashboard wired to current API/demo responses with filters and detail views.
- Methodology, provenance, and implementation tracking docs kept in-repo.

## Roadmap checklist (execution backlog)

### Phase 0 — Governance and definitions

- [ ] Freeze legal semantics for `illegal_today` vs `non_conforming_tolerated`.
- [x] Define confidence levels and uncertainty handling.
- [ ] Approve disclaimer text for public-facing map/dashboard.

### Phase 1 — Data acquisition and canonical model

- [ ] Ingest building footprint sources (Paris + national references).
- [ ] Ingest address points and parcel references.
- [ ] Build deterministic deduplication + entity linking.
- [ ] Version all sources with extraction dates and license metadata.

### Phase 2 — Rule formalization

- [ ] Encode PLU zoning constraints by spatial zone.
- [ ] Encode height/FAR/envelope constraints.
- [x] Encode usage constraints and prohibited uses by zone.
- [ ] Encode heritage/protected perimeter overrides.
- [ ] Encode optional rule packs (accessibility/energy/fire).

### Phase 3 — Evaluation engine

- [x] Implement per-building rule evaluation with explainable trace.
- [x] Add confidence scoring and missing evidence reporting.
- [ ] Store result snapshots with `rule_version` and timestamp.

### Phase 4 — API and map/dashboard UX

- [ ] Build viewport/bbox query endpoint for map rendering.
- [x] Build building detail endpoint with violation explanations.
- [ ] Build stats endpoints by arrondissement/rule category.
- [x] Implement frontend layers and filters.

### Phase 5 — Quality, reproducibility, and ops

- [ ] Add unit + integration + spatial validation tests.
- [ ] Add migration and seed workflows for local/dev/prod.
- [ ] Add CI checks (lint, tests, docs integrity).
- [ ] Add release/versioning strategy for rules and data snapshots.

## Important product notes

- Legality output should support at least:
  - `legal_today`
  - `illegal_today`
  - `unknown_insufficient_data`
  - `non_conforming_tolerated` (if policy requires)
- Every decision must be explainable with machine- and human-readable rationale.
