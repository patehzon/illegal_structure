# ETL scaffold

This module will ingest and normalize all datasets needed to classify building legality in Paris.

## Planned datasets (initial)

- Building footprints / geometry sources
- Address and street number sources
- Parcel/cadastre references
- Zoning and regulatory layers
- Heritage/protection layers

## Pipeline stages

1. `extract`: pull source snapshots with source metadata.
2. `normalize`: convert to canonical schema and CRS.
3. `link`: deduplicate and join building/address/parcel relations.
4. `load`: write to PostGIS staging + curated tables.
5. `validate`: quality checks and anomaly reporting.

Use `etl/scripts/` for executable ingestion modules.

## Runnable MVP skeleton

The current MVP ships a deterministic demo ingestion command that writes staged
JSON outputs with provenance metadata.

```bash
python3 etl/scripts/ingest_placeholder.py \
  --dataset demo_paris_inventory \
  --output-dir etl/staging \
  --extraction-date 2026-03-01 \
  --run-id local-demo
```

Output layout:

- `etl/staging/<dataset>/<extraction-date>/<run-id>/buildings.jsonl`
- `etl/staging/<dataset>/<extraction-date>/<run-id>/manifest.json`

Each staged building record includes a `provenance` object with dataset/source
identity, extraction date, pipeline run id, and source record id so evaluator
outputs can be traced back to the staging layer.
