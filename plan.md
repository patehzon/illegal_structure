## Objective

Turn the scaffold into a working MVP for "Illegal Structure — Paris Building Legality (2026)" with a rule-driven evaluator, backend endpoints wired to that evaluator, a minimal runnable ETL skeleton, aligned docs, and tests that keep behavior explicit and reproducible.

## Scope

In:
- Backend API wiring for listing buildings, building detail evaluation, and stats.
- Rule-driven evaluator behavior using the local catalog and explainability fields.
- Minimal ETL CLI skeleton that emits staged outputs with provenance metadata.
- Documentation updates for assumptions and methodology.
- Test coverage for evaluator and backend endpoints.

Out:
- Real Paris source ingestion or spatial joins.
- Production database/storage layers.
- Full frontend map/dashboard implementation beyond current scaffold.
- Full PLU/legal completeness for all zoning and exception cases.

## Milestones

1. Baseline captured and plan established.
2. Rule evaluator upgraded from placeholder to deterministic catalog-backed MVP.
3. Backend endpoints wired to evaluator with structured responses and tests.
4. ETL runnable skeleton emits reproducible staged records with provenance.
5. Docs and handoff notes aligned with implemented assumptions.

## Ordered Task List

- [x] Review scaffold, roadmap, and current implementation gaps.
- [x] Run baseline `make check` and `make test`; record outputs.
- [x] Implement rule catalog loading and deterministic evaluator rules.
- [x] Expand backend models/endpoints to use evaluator outputs.
- [x] Add backend and evaluator tests covering happy path and failure/unknown cases.
- [x] Implement ETL CLI skeleton with staged JSON output and provenance fields.
- [x] Update methodology/docs to match implemented logic and assumptions.
- [x] Run final checks/tests and summarize remaining work.
- [x] Create focused commits for each completed increment.
- [x] Implement frontend data loading, status rendering, and filters against the current demo API.
- [x] Add the minimum backend browser support needed for local frontend-to-API requests.
- [x] Update `README.md` checklist items to reflect completed roadmap work without overstating scope.
- [x] Verify backend tests and frontend build/dev ergonomics after the UI increment.
- [x] Commit the frontend increment.
- [x] Reproduce and fix backend runtime/bootstrap failures on the real server path.
- [x] Verify the live backend over HTTP after provisioning the project runtime.
- [x] Commit the backend runtime fix.

## Now / Next / Later

Now:
- Commit the verified backend runtime fix and hand off the corrected run path.

Next:
- Expand the rules catalog beyond the current zone/use/height MVP assumptions.
- Add bbox/map-oriented APIs and geometry-backed map rendering.

Later:
- Add bbox/map-oriented endpoints and frontend integration.
- Expand rule packs beyond baseline zoning/use/height logic.
- Add richer ETL source registries and spatial validation.

## Risks & Open Questions

- The current catalog thresholds and allowed-use mappings are MVP assumptions, not yet validated against the full 2026 Paris legal corpus.
- There is no canonical building dataset yet, so backend responses will rely on seeded in-memory demo records for now.
- `non_conforming_tolerated` semantics are unresolved in `README.md`; MVP should avoid inferring that status without explicit evidence.
- The user requested work in `/workspace/illegal_structure`, but this environment only contains `/home/lassouli/illegal_structure`. Work is proceeding in the available repo.

## Baseline Checks

- `2026-03-17`: `make check` -> passed. `python3 -m compileall backend rules etl` completed without errors.
- `2026-03-17`: `make test` -> passed. `python3 -m unittest discover -s backend/tests -p 'test_*.py'` ran 1 test, 0 failures.

## Increment Log

- `2026-03-17` Increment 1: replaced placeholder evaluator logic with catalog-backed zone/use/height checks, added explainability fields (`violations`, `explanations`, `missing_evidence`, `rule_version`, `confidence`), seeded a demo building inventory, and wired `/v1/buildings`, `/v1/buildings/{building_id}`, and `/v1/stats` to live evaluator outputs.
- `2026-03-17` Increment 1 verification: `make check` passed. `make test` passed with 12 tests covering evaluator behavior, health, list/detail handler wiring, filters, stats aggregation, and not-found handling.
- `2026-03-17` Increment 2: replaced the ETL print stub with a runnable staging CLI that writes `buildings.jsonl` and `manifest.json` under `etl/staging/<dataset>/<extraction-date>/<run-id>/`, and updated ETL/data/methodology docs to describe provenance and current evaluator assumptions.
- `2026-03-17` Increment 2 verification: `make check` passed. `make test` passed with 14 tests. `python3 etl/scripts/ingest_placeholder.py --dataset demo_paris_inventory --output-dir /tmp/illegal-structure-stage --extraction-date 2026-03-01 --run-id local-demo` wrote a 5-record staged dataset and manifest successfully.
- `2026-03-17` Increment 3: replaced the placeholder frontend with a filterable legality dashboard that loads `/v1/buildings` and `/v1/stats`, fetches building detail traces, supports local fallback demo data, and added local dev proxy/CORS support plus README roadmap checkmark updates.
- `2026-03-17` Increment 3 verification: `make check` passed. `make test` passed with 14 tests. `npm install` completed successfully in `frontend/`. `npm run build` succeeded and produced a Vite production bundle in `frontend/dist/`.
- `2026-03-17` Increment 4: fixed the backend runtime path by turning `make bootstrap` into a real environment provisioner, routing `make check`, `make test`, and `make run-backend` through the project `.venv`, and upgrading backend pins to Python 3.14-compatible FastAPI/Pydantic/Uvicorn versions.
- `2026-03-17` Increment 4 verification: `make bootstrap` passed. `make check` passed. `make test` passed with 14 tests under `.venv`. Live HTTP probes against `127.0.0.1:8001` returned expected JSON for `/health`, `/v1/buildings`, `/v1/stats`, and `/v1/buildings/PARIS-DEMO-0002`.

## Assumptions

- MVP classifications are deterministic from local building attributes only: `zone_code`, `height_m`, `primary_use`, and optional `heritage_protected`.
- Heritage protection will raise uncertainty rather than produce a hard legality override until rule semantics are formalized in the catalog.
- Demo backend inventory can be stored in code while ETL and persistence are still scaffold-level.
- JSON-formatted content inside `rules/catalog/2026-baseline.yaml` is acceptable for the MVP because JSON is valid YAML 1.2 and keeps the catalog parseable with the Python standard library in this environment.

## Remaining Work

- `non_conforming_tolerated` semantics remain unresolved and are not emitted by the evaluator.
- Rule coverage is intentionally narrow: no spatial zoning joins, parcel logic, heritage overrides beyond manual-review fallback, or bbox map endpoints yet.
- The frontend is inventory/detail oriented for now; it does not yet render real building geometries or viewport-driven map queries.
