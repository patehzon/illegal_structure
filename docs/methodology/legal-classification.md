# Legal classification methodology (draft)

## Objective

Classify whether an existing Paris building would be legal if built under 2026 rules.

## Classification statuses

- `legal_today`
- `illegal_today`
- `unknown_insufficient_data`
- `non_conforming_tolerated`

## Core principles

1. **Explainability first**: every outcome includes machine-readable rule codes and human explanations.
2. **Versioning**: every result references explicit `rule_version`.
3. **Provenance**: all decisions link back to source datasets and extraction dates.
4. **Uncertainty disclosure**: missing critical evidence must downgrade confidence and/or status.

## Confidence bands

- `0.80-1.00`: strong evidence
- `0.50-0.79`: partial evidence
- `<0.50`: weak/incomplete evidence

## MVP rule assumptions implemented now

The current evaluator uses a baseline local catalog and only the following
attributes:

- `zone_code`
- `height_m`
- `primary_use`
- `heritage_protected`

Current MVP behavior:

- Missing `zone_code`, `height_m`, or `primary_use` -> `unknown_insufficient_data`
- Zone/use incompatibility -> `illegal_today`
- Zone height exceedance -> `illegal_today`
- Heritage-protected building with no base violation -> `unknown_insufficient_data`
- Fully compliant non-heritage building -> `legal_today`

The evaluator emits:

- `violations`: machine-readable failed rule checks
- `explanations`: pass/fail/unknown trace for each evaluated rule
- `missing_evidence`: unresolved fields or manual-review gaps
- `rule_version`: currently `2026-baseline`
- `confidence`: deterministic confidence tied to evidence completeness

`non_conforming_tolerated` remains intentionally unused until policy semantics
are frozen.

## Public communication constraints

- Avoid definitive legal claims where evidence is incomplete.
- Present this as a decision-support map, not legal advice.
- Provide clear route for data correction and appeals.
