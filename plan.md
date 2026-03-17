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
- [ ] Implement ETL CLI skeleton with staged JSON output and provenance fields.
- [ ] Update methodology/docs to match implemented logic and assumptions.
- [ ] Run final checks/tests and summarize remaining work.
- [ ] Create focused commits for each completed increment.

## Now / Next / Later

Now:
- Implement ETL CLI skeleton with reproducible staged output.
- Update methodology/docs to reflect the implemented evaluator assumptions.

Next:
- Evaluate whether the frontend scaffold should consume local API/demo responses in the next increment.
- Add more rule catalog coverage only after the current assumptions are documented.

Later:
- Add bbox/map-oriented endpoints and frontend integration.
- Expand rule packs beyond baseline zoning/use/height logic.
- Add richer ETL source registries and spatial validation.

## Risks & Open Questions

- The current YAML catalog only lists rule metadata, not executable thresholds; MVP will need documented assumptions for zone/use constraints.
- There is no canonical building dataset yet, so backend responses will rely on seeded in-memory demo records for now.
- `non_conforming_tolerated` semantics are unresolved in `README.md`; MVP should avoid inferring that status without explicit evidence.
- The user requested work in `/workspace/illegal_structure`, but this environment only contains `/home/lassouli/illegal_structure`. Work is proceeding in the available repo.

## Baseline Checks

- `2026-03-17`: `make check` -> passed. `python3 -m compileall backend rules etl` completed without errors.
- `2026-03-17`: `make test` -> passed. `python3 -m unittest discover -s backend/tests -p 'test_*.py'` ran 1 test, 0 failures.

## Increment Log

- `2026-03-17` Increment 1: replaced placeholder evaluator logic with catalog-backed zone/use/height checks, added explainability fields (`violations`, `explanations`, `missing_evidence`, `rule_version`, `confidence`), seeded a demo building inventory, and wired `/v1/buildings`, `/v1/buildings/{building_id}`, and `/v1/stats` to live evaluator outputs.
- `2026-03-17` Increment 1 verification: `make check` passed. `make test` passed with 12 tests covering evaluator behavior, health, list/detail handler wiring, filters, stats aggregation, and not-found handling.

## Assumptions

- MVP classifications are deterministic from local building attributes only: `zone_code`, `height_m`, `primary_use`, and optional `heritage_protected`.
- Heritage protection will raise uncertainty rather than produce a hard legality override until rule semantics are formalized in the catalog.
- Demo backend inventory can be stored in code while ETL and persistence are still scaffold-level.
- JSON-formatted content inside `rules/catalog/2026-baseline.yaml` is acceptable for the MVP because JSON is valid YAML 1.2 and keeps the catalog parseable with the Python standard library in this environment.
