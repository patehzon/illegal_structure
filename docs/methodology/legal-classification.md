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

## Public communication constraints

- Avoid definitive legal claims where evidence is incomplete.
- Present this as a decision-support map, not legal advice.
- Provide clear route for data correction and appeals.
